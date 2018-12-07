Name: grpc
Version: 1.17.0
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

Patch0: 0001-enforce-system-crypto-policies.patch
# https://github.com/grpc/grpc/pull/15532
Patch1: 0002-patch-from-15532.patch

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

%prep
%autosetup -p1
sed -i 's:^prefix ?= .*:prefix ?= %{_prefix}:' Makefile
sed -i 's:$(prefix)/lib:$(prefix)/%{_lib}:' Makefile
sed -i 's:^GTEST_LIB =.*::' Makefile

%build
%make_build shared plugins

%install
make install prefix="%{buildroot}%{_prefix}"
make install-grpc-cli prefix="%{buildroot}%{_prefix}"
find %{buildroot} -type f -name '*.a' -exec rm -f {} \;

%ldconfig_scriptlets

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

%changelog
* Fri Dec 07 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.0-1
- Initial revision
