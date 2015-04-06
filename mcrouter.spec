# TODO:
# - compile fails: undefined reference to `jump_fcontext', check boost-context.patch for proper fix
%define	gitrev	39a7572
Summary:	Memcached protocol router for scaling memcached deployments
Name:		mcrouter
# version from configure.ac
Version:	1.0
Release:	0.1
License:	BSD
Group:		Daemons
Source0:	https://github.com/facebook/mcrouter/archive/%{gitrev}/%{name}-%{gitrev}.tar.gz
# Source0-md5:	f99eb19ccd41169e9570ca2b1d152b8a
Patch0:		boost-context.patch
URL:		https://github.com/facebook/mcrouter
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.51.0
BuildRequires:	double-conversion-devel
BuildRequires:	folly-devel >= 0.31
BuildRequires:	gflags-devel
BuildRequires:	glog-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	ragel
# needs folly, which builds on x86-64 only
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mcrouter is a memcached protocol router for scaling memcached
<http://memcached.org/> deployments. It's a core component of cache
infrastructure at Facebook and Instagram where mcrouter handles almost
5 billion requests per second at peak.

%prep
%setup -qc
mv mcrouter-*/* .
%patch0 -p1

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
%attr(755,root,root) %{_bindir}/mcrouter
