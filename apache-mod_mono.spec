%define xsp_version 0.4
Summary:	Mono module for Apache 2
Summary(pl):	Modu³ Mono dla serwera Apache 2
Name:		mod_mono
Version:	0.3
Release:	2
Epoch:		1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.apacheworld.org/modmono/%{name}-%{version}.tar.gz
# Source0-md5:	c28a82496cf87de3c91450e47a4efcf1
Source1:	http://go-mono.com/archive/xsp-%{xsp_version}.tar.gz
# Source1-md5:	aacb2d6b0dc3f54382c09be0976f6a7f
Source2:	mono.conf
URL:		http://www.apacheworld.org/modmono/
BuildRequires:	apache-devel >= 2.0
BuildRequires:	autoconf
BuildRequires:	mono
Requires:	apache >= 2.0
#Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		httpdir		/home/services/httpd
%define		htmldir		%{httpdir}/html
%define		moddir		/usr/lib/apache

%description
This is an experimental module that allows you to run ASP.NET pages on
Unix with Apache and Mono.

%description -l pl
Ten eksperymentalny modu³ umo¿liwia uruchamianie stron ASP.NET na
Uniksie z serwerem Apache i Mono.

%prep
%setup -q -n %{name}-%{version} -a 1

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd/conf.d,%{moddir}} \
	$RPM_BUILD_ROOT%{htmldir}/{mono,.wapi}

cp %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install src/.libs/libmod_mono.so $RPM_BUILD_ROOT%{moddir}
install src/ModMono.dll $RPM_BUILD_ROOT%{_libdir}
cp -r xsp-%{xsp_version}/server/test/* $RPM_BUILD_ROOT%{htmldir}/mono

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README
%attr(755,root,root) %{moddir}/libmod_mono.so
%{_libdir}/ModMono.dll
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/conf.d/mono.conf
# FIXME
%defattr(-,http,http)
%{htmldir}/mono
%{httpdir}/.wapi
