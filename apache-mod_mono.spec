%define pkg_version 0.3
%define xsp_version 0.3
Summary:	Mono module for Apache 2
Summary(pl):	Modu³ Mono dla serwera Apache 2
Name:		mod_mono
Version:	0.3.6
Release:	1
License:	The Apache License
Group:		Networking/Daemons
Source0:	http://www.apacheworld.org/modmono/%{name}-%{pkg_version}.tar.gz
Source1:	xsp-%{xsp_version}.tar.gz
Source2:	mono.conf
BuildRequires:	autoconf
BuildRequires:	apache-devel
BuildRequires:	mono
Requires:	apache
#Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		httpdir		/home/services/httpd
%define		htmldir		%{httpdir}/html
%define		moddir		/usr/lib/apache

%description
This module allows you to run ASP.NET pages on Unix with Apache and
Mono.

%description -l pl
Ten modu³ umo¿liwia uruchamianie stron ASP.NET na Uniksie z serwerem
Apache i Mono.

%prep
%setup -q -n %{name}-%{pkg_version} -a 1

%build
# Build sample ASP.NET pages from xsp distribution
cd xsp-%{xsp_version}
%{__make}
%{__make} install
cd ..

# Build Apache Module
%{__autoconf}
%configure \
	--with-apxs=%{_sbindir}/apxs
%{__make}

# Build Mono DLL
%{__make} -C src -f makedll.mak

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -d $RPM_BUILD_ROOT%{moddir}
install -d $RPM_BUILD_ROOT%{htmldir}/mono
install -d $RPM_BUILD_ROOT%{httpdir}/.wapi

cp %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install src/.libs/libmod_mono.so $RPM_BUILD_ROOT%{moddir}
install src/ModMono.dll $RPM_BUILD_ROOT%{_libdir}
cp -r xsp-%{xsp_version}/server/test/* $RPM_BUILD_ROOT%{htmldir}/mono

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING INSTALL NEWS README
%attr(755,root,root) %{moddir}/libmod_mono.so
%{_libdir}/ModMono.dll
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/conf.d/mono.conf
# FIXME
%defattr(-,http,http)
%{htmldir}/mono
%{httpdir}/.wapi
