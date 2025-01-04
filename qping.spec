%define name gping
%define version 1.19.0
%define release 1%{?dist}

Summary:  Ping, but with a graph
Name:     %{name}
Version:  %{version}
Release:  %{release}
License:  MIT License
URL:      https://github.com/orf/gping
Source0:  https://github.com/orf/gping/archive/refs/tags/gping-v%{version}.tar.gz

%define debug_package %{nil}

BuildRequires: curl
BuildRequires: gcc
BuildRequires: make
BuildRequires: gzip
BuildRequires: upx

%description
Ping, but with a graph.

%prep
%setup -q -n gping-gping-v%{version}

%build
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
cargo build --release
strip --strip-all target/release/%{name}
mkdir -p %{buildroot}/%{_mandir}/man1/
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_bindir}
gzip %{name}.1
upx target/release/%{name}

%install
# Create necessary directories
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_mandir}/man1/

# Install the binary and man page
install -m 755 target/release/%{name} %{buildroot}/%{_bindir}/
install -Dpm 0644 %{name}.1.gz -t %{buildroot}/%{_mandir}/man1/

%files
%license LICENSE
%doc readme.md
# List all the files to be included in the package
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Sat Jan 4 2025 - Danie de Jager - 1.19.0-1
* Mon Nov 18 2024 - Danie de Jager - 1.18.0-2
* Mon Oct 21 2024 - Danie de Jager - 1.17.3-2
* Mon Jul 22 2024 - Danie de Jager - 1.17.3-1
* Fri Jul 12 2024 - Danie de Jager - 1.16.1-2
- rebuilt with Rust 1.79.0
* Sun Apr 14 2024 - Danie de Jager - 1.16.1-1
- Initial RPM build
