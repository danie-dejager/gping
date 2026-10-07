use std::{iter::Iterator, str::FromStr};

use anyhow::{anyhow, Result};
use tui::style::Color;

/// Palette indices that are black or near-black and vanish on a dark terminal background.
fn is_hard_to_see(index: u8) -> bool {
    matches!(index, 0 | 8 | 16..=19 | 232..=239)
}

pub struct Colors<T> {
    already_used: Vec<Color>,
    color_names: T,
    next_index: u8,
    wrapped: bool,
}

impl<T> From<T> for Colors<T> {
    fn from(color_names: T) -> Self {
        Self {
            already_used: Vec::new(),
            color_names,
            next_index: 2,
            wrapped: false,
        }
    }
}

impl<'a, T> Iterator for Colors<T>
where
    T: Iterator<Item = &'a String>,
{
    type Item = Result<Color>;

    fn next(&mut self) -> Option<Self::Item> {
        match self.color_names.next() {
            Some(name) => match Color::from_str(name) {
                Ok(color) => {
                    if !self.already_used.contains(&color) {
                        self.already_used.push(color);
                    }
                    Some(Ok(color))
                }
                error => Some(error.map_err(|err| {
                    anyhow!(err).context(format!("Invalid color code: `{}`", name))
                })),
            },
            None => loop {
                let index = self.next_index;
                if index == u8::MAX {
                    self.next_index = 2;
                    self.wrapped = true;
                } else {
                    self.next_index += 1;
                }
                if is_hard_to_see(index) {
                    continue;
                }
                let color = Color::Indexed(index);
                // After a full lap every color is taken, so reuse is expected.
                if self.wrapped || !self.already_used.contains(&color) {
                    self.already_used.push(color);
                    break Some(Ok(color));
                }
            },
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generated_colors_are_never_hard_to_see() {
        let names: Vec<String> = vec![];
        for color in Colors::from(names.iter()).take(600) {
            match color.unwrap() {
                Color::Indexed(i) => assert!(!is_hard_to_see(i), "index {}", i),
                other => panic!("unexpected color {:?}", other),
            }
        }
    }

    #[test]
    fn test_generated_colors_cycle_without_panicking() {
        let names: Vec<String> = vec![];
        assert_eq!(Colors::from(names.iter()).take(1000).count(), 1000);
    }
}
