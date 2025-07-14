Summary:	Memcached protocol router for scaling memcached deployments
Name:		mcrouter
Version:	0.1.0
Release:	1.1
License:	BSD
Group:		Daemons
Source0:	https://github.com/facebook/mcrouter/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5cc3e44ee2ff027e8b4077494222610c
Patch0:		am-subdir-objects.patch
Patch1:		shared-lib.patch
URL:		https://github.com/facebook/mcrouter
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.51.0
BuildRequires:	double-conversion-devel
BuildRequires:	folly-devel >= 0.41.0
BuildRequires:	gflags-devel
BuildRequires:	glog-devel
BuildRequires:	libcap-devel
BuildRequires:	libevent-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	ragel
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
# needs folly, which builds on x86-64 only
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# it links to -lfolly, but still symbols seem missing. meh
%define		skip_post_check_so	libmcroutercore.so.0.0.0 libmcrouter.so.0.0.0

%description
Mcrouter is a memcached protocol router for scaling memcached
<http://memcached.org/> deployments. It's a core component of cache
infrastructure at Facebook and Instagram where mcrouter handles almost
5 billion requests per second at peak.

%package libs
Summary:	mcrouter shared libraries
Group:		Libraries

%description libs
mcrouter shared libraries.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE PATENTS
%attr(755,root,root) %{_bindir}/mcrouter

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmcrouter.so.*.*.*
%ghost %{_libdir}/libmcrouter.so.0
%attr(755,root,root) %{_libdir}/libmcroutercore.so.*.*.*
%ghost %{_libdir}/libmcroutercore.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmcrouter.la
%{_libdir}/libmcrouter.so
%{_libdir}/libmcroutercore.la
%{_libdir}/libmcroutercore.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libmcrouter.a
%{_libdir}/libmcroutercore.a
