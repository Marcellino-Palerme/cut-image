%define _build_id_links none
Summary:cut images
Name: cuti
Version: 1.3
Release: 1
License: CeCILL 2.1
Group: File tools
SOURCE0 : %{name}

Requires: libxcb python3-tkinter
%description
%{summary}

%prep

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%{_bindir}/%{name}
