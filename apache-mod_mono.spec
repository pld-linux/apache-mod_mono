# TODO:
# - figure out how to kill mod-mono-server.exe process when apache is restarted
%define		mod_name	mod_mono
%define 	apxs		/usr/sbin/apxs
Summary:	Mono module for Apache 2
Summary(pl.UTF-8):	Moduł Mono dla serwera Apache 2
Name:		apache-%{mod_name}
Version:	1.1.10
Release:	1
Epoch:		1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.go-mono.com/sources/%{mod_name}/%{mod_name}-%{version}.tar.gz
# Source0-md5:	ff71db2750f7ef50f57f85dc6f593373
Patch0:		%{name}-apu-config.patch
Patch1:		%{name}-apr_fixes.patch
URL:		http://www.mono-project.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 1.0
BuildRequires:	pkgconfig
Requires:	apache(modules-api) = %apache_modules_api
Requires:	mono-csharp >= 1.0
Requires:	xsp
Obsoletes:	mod_mono
ExcludeArch:	alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_httpdir	/home/services/httpd
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an experimental module that allows you to run ASP.NET pages on
Unix with Apache and Mono.

%description -l pl.UTF-8
Ten eksperymentalny moduł umożliwia uruchamianie stron ASP.NET na
Uniksie z serwerem Apache i Mono.

%prep
%setup -q -n %{mod_name}-%{version}
%patch0 -p1
%patch1 -p1

%build
# Build Apache Module
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-apxs=%{apxs} \
	--with-apr-config=%{_bindir}/apr-1-config \
	--with-apu-config=%{_bindir}/apu-1-config \
	CFLAGS="%{rpmcflags} -D_GNU_SOURCE -D_LARGEFILE64_SOURCE"

%{__make} \
	DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd.conf,%{_pkglibdir},%{_mandir}/man8}

install src/.libs/%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install man/%{mod_name}.8 $RPM_BUILD_ROOT%{_mandir}/man8

cat > $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/70_mod_%{mod_name}.conf <<EOF
LoadModule mono_module modules/%{mod_name}.so
MonoApplications "/asp_net:%{_httpdir}/asp_net"
Alias /asp_net "%{_httpdir}/asp_net"
<Location /asp_net>
	SetHandler mono
</Location>
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%{_mandir}/man8/*
