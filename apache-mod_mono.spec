
# TODO : figure out how to kill mod-mono-server.exe process 
#	 when apache is restarted

%define		mod_name mod_mono
Summary:	Mono module for Apache 2
Summary(pl):	Modu³ Mono dla serwera Apache 2
Name:		apache-mod_mono
Version:	1.0.1
Release:	0.9
Epoch:		1
License:	Apache
Group:		Networking/Daemons
Source0:	http://mono2.ximian.com/archive/%{version}/%{mod_name}-%{version}.tar.gz
# Source0-md5:	5adb398b270865c484cea53b79e3def4
Patch0:		%{name}-apu-config.patch
URL:		http://www.mono-project.com/
BuildRequires:	apache-devel >= 2.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 1.0
Requires:	xsp
Requires:	apache >= 2.0
Requires:	mono-csharp >= 1.0
Obsoletes:	mod_mono
ExcludeArch:	alpha
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

%package -n dotnet-xsp
Summary:	Mono ASP.NET Standalone Web Server
Summary(pl):	Server HTTP obs³uguj±cy ASP.NET
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	mono-csharp >= 1.0

%description -n dotnet-xsp
Provides a minimalistic web server which hosts the ASP.NET runtime and 
can be used to test and debug web applications that use the System.Web
facilities in  Mono.

%prep
%setup -q -n %{mod_name}-%{version}
%patch0 -p1

%build
rm -rf $RPM_BUILD_ROOT
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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd/httpd.conf,%{_pkglibdir},%{_mandir}/man8}

install src/.libs/libmod_mono.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_mono.so
install src/ModMono.dll $RPM_BUILD_ROOT%{_libdir}
install man/mod_mono.8 $RPM_BUILD_ROOT%{_mandir}/man8

cat > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/70_mod_mono.conf <<EOF
LoadModule mono_module modules/mod_mono.so
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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/*
%doc ChangeLog INSTALL NEWS README
%attr(755,root,root) %{_pkglibdir}/mod_mono.so
%attr(755,root,root) %{_libdir}/ModMono.dll
%{_mandir}/man8/*
