%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Summary:cut images
Name: cuti
Version: 1.3
Release: 1
License: CeCILL 2.1
Group: File tools
SOURCE0 : %{name}-%{version}.tar.gz
BuildRoot: .
Requires: libxcb python3-tkinter
%description
%{summary}

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}
cp -a * %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_bindir}/*
