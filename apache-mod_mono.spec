%define		mod_name mod_mono
%define 	xsp_version 1.0

Summary:	Mono module for Apache 2
Summary(pl):	Modu³ Mono dla serwera Apache 2
Name:		apache-mod_mono
Version:	1.0
Release:	0.9
Epoch:		1
License:	Apache
Group:		Networking/Daemons
Source0:	http://mono2.ximian.com/archive/1.0/%{mod_name}-%{version}.tar.gz
# Source0-md5:	154720f6286105d513d1688f4a6e2b29
Source1:	http://mono2.ximian.com/archive/1.0/xsp-%{xsp_version}.tar.gz
# Source1-md5:	cd681f02d0f93774ba126d77fd377f4b
Patch0:		%{name}-apu-config.patch
URL:		http://www.mono-project.com/
BuildRequires:	apache-devel >= 2.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mono
Requires:	apache >= 2.0
Obsoletes:	mod_mono
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	apxs		%{_sbindir}/apxs
%define		_httpdir	/home/services/httpd
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an experimental module that allows you to run ASP.NET pages on
Unix with Apache and Mono.

%description -l pl
Ten eksperymentalny modu³ umo¿liwia uruchamianie stron ASP.NET na
Uniksie z serwerem Apache i Mono.

%prep
%setup -q -n %{mod_name}-%{version} -a 1
%patch0 -p1

%build
rm -rf $RPM_BUILD_ROOT
# Build sample ASP.NET pages from xsp distribution
cd xsp-%{xsp_version}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-apxs=%{apxs}
	
%{__make} \
	DESTDIR=$RPM_BUILD_ROOT
	
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

# Build Apache Module
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-apxs=%{apxs} \
	--with-apr-config=%{_bindir}/apr-config \
	--with-apu-config=%{_bindir}/apu-config
	
%{__make} \
	DESTDIR=$RPM_BUILD_ROOT

# Build Mono DLL
%{__make} -C src -f makedll.mak

%install
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd/httpd.conf,%{_pkglibdir}} \
	$RPM_BUILD_ROOT%{_httpdir}/{.wapi,mono}

install src/.libs/libmod_mono.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_mono.so
install src/ModMono.dll $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT%{_docdir}/xsp/test $RPM_BUILD_ROOT%{_httpdir}/mono

cat > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/70_mod_mono.conf <<EOF
LoadModule mono_module modules/mod_mono.so
MonoApplications "/mono/test:%{_httpdir}/mono/test"
Alias /mono/test "%{_httpdir}/mono/test"
<Location /mono/test>
    SetHandler mono
</Location>
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README
%attr(755,root,root) %{_pkglibdir}/mod_mono.so
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.dll
%{_mandir}/man1/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/*
%attr(750,http,http) %{_httpdir}/.wapi
%defattr(644,http,http,755)
%{_httpdir}/mono
