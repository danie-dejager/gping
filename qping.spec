%define name qping
%define version 1.16.1
%define release 1%{?dist}

Summary:  Ping, but with a graph
Name:     %{name}
Version:  %{version}
Release:  %{release}
License:  MIT License
URL:      https://github.com/orf/gping
Source0:  https://github.com/orf/gping/archive/refs/tags/gping-v%{Version}.tar.gz

%define debug_package %{nil}

BuildRequires: curl
BuildRequires: gcc
BuildRequires: make
BuildRequires: gzip

%description
Ping, but with a graph.

%prep
%setup -q

%build
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
cargo build --release
strip --strip-all target/release/%{name}
# Install manpages
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_bindir}/
gzip doc/%{name}.1

%install
install -Dpm 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 doc/%{name}.1.gz -t %{buildroot}%{_mandir}/man1/

# Copy the binary to /bin in the buildroot
install -m 755 target/release/%{name} %{buildroot}/%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md CHANGELOG.md
# List all the files to be included in the package
%{_bindir}/%{name}
%{_sysconfdir}/fish/vendor_completions.d/%{name}.fish
%{_sysconfdir}/zsh/site-functions/_%{name}
%{_sysconfdir}/bash_completion.d/%{name}.bash
%{_mandir}/man1/%{name}.1.gz

%changelog
* Sun Apr 14 2024 - Danie de Jager - 1.16.1-1
- Initial RPM build
