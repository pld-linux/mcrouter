Summary:	Memcached protocol router for scaling memcached deployments
Name:		mcrouter
Version:	0.1.0
Release:	1
License:	BSD
Group:		Daemons
Source0:	https://github.com/facebook/mcrouter/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5cc3e44ee2ff027e8b4077494222610c
URL:		https://github.com/facebook/mcrouter
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.51.0
BuildRequires:	double-conversion-devel
BuildRequires:	folly-devel >= 0.41.0
BuildRequires:	gflags-devel
BuildRequires:	glog-devel
BuildRequires:	libcap-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	ragel
BuildRequires:	zlib-devel
# needs folly, which builds on x86-64 only
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mcrouter is a memcached protocol router for scaling memcached
<http://memcached.org/> deployments. It's a core component of cache
infrastructure at Facebook and Instagram where mcrouter handles almost
5 billion requests per second at peak.

%prep
%setup -q

%build
cd mcrouter
%{__aclocal} -I m4
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -C mcrouter \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE PATENTS
%attr(755,root,root) %{_bindir}/mcrouter
