# TODO:
# - figure out how to kill mod-mono-server.exe process when apache is restarted
%define		mod_name	mod_mono
%define		apxs		/usr/sbin/apxs
Summary:	Mono module for Apache 2
Summary(pl.UTF-8):	Moduł Mono dla serwera Apache 2
Name:		apache-%{mod_name}
Version:	3.13
Release:	1
Epoch:		1
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	https://download.mono-project.com/sources/mod_mono/%{mod_name}-%{version}.tar.gz
# Source0-md5:	81f6c9ca314c239e0b4634eedf174ced
Patch0:		apache-mod_mono-ac.patch
URL:		https://www.mono-project.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 3.12
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.015
Requires:	apache(modules-api) = %apache_modules_api
Requires:	mono-csharp >= 3.12
Requires:	xsp >= 2.10
Obsoletes:	mod_mono < 1:0.3.7
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_httpdir	/home/services/httpd
%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
This is an experimental module that allows you to run ASP.NET pages on
Unix with Apache and Mono.

%description -l pl.UTF-8
Ten eksperymentalny moduł umożliwia uruchamianie stron ASP.NET na
Uniksie z serwerem Apache i Mono.

%prep
%setup -q -n %{mod_name}-%{version}
%patch -P0 -p1

%build
# Build Apache Module
%{__libtoolize}
%{__aclocal}
%{__autoconf} -I m4
%{__automake}

%configure \
	CFLAGS="%{rpmcflags} -D_GNU_SOURCE -D_LARGEFILE64_SOURCE" \
	--with-apxs=%{apxs} \
	--with-apr-config=%{_bindir}/apr-1-config \
	--with-apu-config=%{_bindir}/apu-1-config

%{__make} \
	DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apacheconfdir},%{apachelibdir},%{_mandir}/man8}

install src/.libs/%{mod_name}.so $RPM_BUILD_ROOT%{apachelibdir}
install man/%{mod_name}.8 $RPM_BUILD_ROOT%{_mandir}/man8

cat > $RPM_BUILD_ROOT%{apacheconfdir}/70_mod_%{mod_name}.conf <<'EOF'
LoadModule mono_module modules/%{mod_name}.so
MonoApplications "/asp_net:%{_httpdir}/asp_net"
Alias /asp_net "%{_httpdir}/asp_net"
<Location /asp_net>
	SetHandler mono
</Location>
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
    %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{apachelibdir}/mod_mono.so
%{_mandir}/man8/mod_mono.8*
