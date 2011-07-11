%define		trac_ver	0.11
%define		plugin		autocompleteusers
%define		revision	10429
Summary:	Autocomplete user fields (assigned to and CC) on tickets
Name:		trac-plugin-%{plugin}
Version:	0.4.1
Release:	0.r%{revision}
License:	BSD
Group:		Applications/WWW
# Source0Download:	http://trac-hacks.org/changeset/latest/autocompleteusersplugin?old_path=/&filename=autocompleteusersplugin&format=zip
Source0:	%{plugin}plugin-r%{revision}.zip
# Source0-md5:	8c28c08ec2314721c82ffc61358476c7
URL:		http://trac-hacks.org/wiki/AutocompleteUsersPlugin
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The AutocompleteUsersPlugin allows AJAX completion of users for the
owner and CC fields on new and existing tickets. Currently, all the
known users are autocompleted though this could be restricted to those
that have the ticket owner permission. A /users URL is served which
presents the user data in a format suitable to the javascript
autocompleter.

%prep
%setup -q -n %{plugin}plugin

%build
cd %{trac_ver}
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
cd %{trac_ver}
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable the %{plugin} plugin, add to conf/trac.ini:

	[components]
	%{plugin}.* = enabled
EOF
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/AutocompleteUsers-*.egg-info
