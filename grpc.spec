%if 0%{?fedora} || 0%{?rhel} > 7
# Do not build python3 subpackage on EL7 and python2 on El > 8
%bcond_without python3
%bcond_with python2
%else
%bcond_with python3
%bcond_without python2
%endif

Name: grpc
Version: 1.20.1
Release: 1%{?dist}
Summary: Modern, open source, high-performance remote procedure call (RPC) framework
License: ASL 2.0
URL: https://www.grpc.io
Source0: https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: pkgconfig
BuildRequires: protobuf-devel
BuildRequires: protobuf-compiler
BuildRequires: openssl-devel
BuildRequires: c-ares-devel
BuildRequires: gflags-devel
BuildRequires: gtest-devel
BuildRequires: zlib-devel
BuildRequires: gperftools-devel

%if %{with python2}
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-Cython
%endif

%if %{with python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-Cython
%endif

Patch0: grpc-0001-enforce-system-crypto-policies.patch
# https://github.com/grpc/grpc/pull/17732
# Patch3: 0003-tcp_posix.cc-fix-typo-in-bitwise-condition.patch
Patch2: grpc-0003-use-shell-loop-instead-makefile-function.patch
Patch4: grpc-0004-DISABLE-ARES.patch

%description
gRPC is a modern open source high performance RPC framework that can run in any
environment. It can efficiently connect services in and across data centers
with pluggable support for load balancing, tracing, health checking and
authentication. It is also applicable in last mile of distributed computing to
connect devices, mobile applications and browsers to backend services.

The main usage scenarios:

* Efficiently connecting polyglot services in microservices style architecture
* Connecting mobile devices, browser clients to backend services
* Generating efficient client libraries

Core Features that make it awesome:

* Idiomatic client libraries in 10 languages
* Highly efficient on wire and with a simple service definition framework
* Bi-directional streaming with http/2 based transport
* Pluggable auth, tracing, load balancing and health checking


%package plugins
Summary: gRPC protocol buffers compiler plugins
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: protobuf-compiler

%description plugins
Plugins to the protocol buffers compiler to generate gRPC sources.

%package cli
Summary: gRPC protocol buffers cli
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cli
Plugins to the protocol buffers compiler to generate gRPC sources.

%package devel
Summary: gRPC library development files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and files for gRPC libraries.

%if %{with python2}
%package -n python2-grpcio
Summary: Python language bindings for grpc, remote procedure call (RPC) framework
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-grpcio
Python2 bindings for gRPC library.
%endif

%if %{with python3}
%package -n python3-grpcio
Summary: Python language bindings for grpc, remote procedure call (RPC) framework
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-grpcio
Python3 bindings for gRPC library.
%endif

%prep
%autosetup -N
%patch0 -p1
%patch2 -p1
%patch4 -p1
sed -i 's:^prefix ?= .*:prefix ?= %{_prefix}:' Makefile
sed -i 's:$(prefix)/lib:$(prefix)/%{_lib}:' Makefile
sed -i 's:^GTEST_LIB =.*::' Makefile

%build
%make_build shared plugins

# build python module
export GRPC_PYTHON_BUILD_WITH_CYTHON=True
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=True
export GRPC_PYTHON_BUILD_SYSTEM_CARES=True
export CFLAGS="%optflags"
%if %{with python3}
%py3_build
%endif
%if %{with python2}
%py2_build
%endif

%install
make install prefix="%{buildroot}%{_prefix}"
make install-grpc-cli prefix="%{buildroot}%{_prefix}"
find %{buildroot} -type f -name '*.a' -exec rm -f {} \;
%if %{with python3}
%py3_install
%endif
%if %{with python2}
%py2_install
%endif

%if 0%{?fedora} || 0%{?rhel} > 7
%ldconfig_scriptlets
%else
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

%files
%doc README.md
%license LICENSE
%{_libdir}/*.so.1*
%{_libdir}/*.so.7*
%{_datadir}/grpc

%files cli
%{_bindir}/grpc_cli

%files plugins
%doc README.md
%license LICENSE
%{_bindir}/grpc_*_plugin

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/grpc
%{_includedir}/grpc++
%{_includedir}/grpcpp

%if %{with python2}
%files -n python2-grpcio
%license LICENSE
%{python2_sitearch}/grpc
%{python2_sitearch}/grpcio-%{version}-py?.?.egg-info
%endif

%if %{with python3}
%files -n python3-grpcio
%license LICENSE
%{python3_sitearch}/grpc
%{python3_sitearch}/grpcio-%{version}-py?.?.egg-info
%endif

%changelog
* Fri May 17 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.20.1-1
- Update to 1.20.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.18.0-1
- Update to 1.18.0

* Mon Dec 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.17.1-3
- Properly store patch in SRPM

* Mon Dec 17 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.1-2
- Build without ruby plugin for Fedora < 30 (Thanks to Mathieu Bridon)

* Fri Dec 14 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.1-1
- Update to 1.17.1 and package python bindings

* Fri Dec 07 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.0-1
- Initial revision
