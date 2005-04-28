#
# TODO:
# - figure out how to kill mod-mono-server.exe process
#   when apache is restarted
#
%define		_name		mod_mono
%define 	apxs		/usr/sbin/apxs
Summary:	Mono module for Apache 2
Summary(pl):	Modu³ Mono dla serwera Apache 2
Name:		apache-%{_name}
Version:	1.0.8
Release:	1
Epoch:		1
License:	Apache
Group:		Networking/Daemons
Source0:	http://mono2.ximian.com/archive/%{version}/%{_name}-%{version}.tar.gz
# Source0-md5:	1189556bafb68cbff4dc601666617de1
Patch0:		%{name}-apu-config.patch
Patch1:		%{name}-apr_fixes.patch
URL:		http://www.mono-project.com/
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	%{apxs}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 1.0
Requires:	xsp
Requires:	apache >= 2.0.52-2
Requires:	mono-csharp >= 1.0
Obsoletes:	mod_mono
ExcludeArch:	alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_httpdir	/home/services/httpd
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define     _sysconfdir /etc/httpd

%description
This is an experimental module that allows you to run ASP.NET pages on
Unix with Apache and Mono.

%description -l pl
Ten eksperymentalny modu³ umo¿liwia uruchamianie stron ASP.NET na
Uniksie z serwerem Apache i Mono.

%prep
%setup -q -n %{_name}-%{version}
%patch0 -p1
%patch1 -p1

%build
rm -rf $RPM_BUILD_ROOT
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

install src/.libs/%{_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/%{_name}.so
install man/%{_name}.8 $RPM_BUILD_ROOT%{_mandir}/man8

cat > $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/70_%{_name}.conf <<EOF
LoadModule mono_module modules/%{_name}.so
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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd.conf/*
%doc ChangeLog INSTALL NEWS README
%attr(755,root,root) %{_pkglibdir}/%{_name}.so
%{_mandir}/man8/*
