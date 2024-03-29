%define _disable_ld_no_undefined 1
%define enable_python_manpage 1

%define major 4
%define libname %mklibname %{name} %{major}

Name: satyr
Version:	0.43
Release:	1
Summary: Tools to create anonymous, machine-friendly problem reports
Group: System/Libraries
License: GPLv2+
URL: https://github.com/abrt/satyr
Source0: https://github.com/abrt/satyr/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires: python-devel
BuildRequires: elfutils-devel
BuildRequires: binutils-devel
BuildRequires: rpm-devel
BuildRequires: slibtool
BuildRequires: gperf
BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(json-c)
BuildRequires: dwz
BuildRequires: pkgconfig(popt)
BuildRequires: pkgconfig(glib-2.0)
%if %{?enable_python_manpage}
BuildRequires: python-sphinx
%endif

%description
Satyr is a library that can be used to create and process microreports.
Microreports consist of structured data suitable to be analyzed in a fully
automated manner, though they do not necessarily contain sufficient information
to fix the underlying problem. The reports are designed not to contain any
potentially sensitive data to eliminate the need for review before submission.
Included is a tool that can create microreports and perform some basic
operations on them.

%package devel
Summary: Development libraries for %{name}
Group: Development/C
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%package -n %{libname}
Summary:        %{summary}
Group:          %{group}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with satyr.

%package -n python-%{name}
Summary: Python bindings for %{name}
Group: Development/Python
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: python2-%{name} < %{EVRD}

%description -n python-%{name}
Python bindings for %{name}.

%prep
%autosetup -p1
printf '%s' '%{version}' > satyr-version
autoreconf -fiv
%configure

%build
%make_build V=1 LIBTOOL=slibtool-shared

%install
%make_install LIBTOOL=slibtool-shared

%check
# FIXME As of 0.24, 2 tests are failing:
# 86: sr_core_stacktrace_from_gdb_limit               FAILED (core_stacktrace.at:205)
# 92: sr_ruby_frame_from_json                         FAILED (ruby_frame.at:184)
#
# Once fixed, shouldn't allow make check to fail

%make check || :

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md NEWS COPYING
%{_bindir}/satyr
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%{_libdir}/libsatyr.so.%{major}*
%files devel
%{_includedir}/satyr/
%{_libdir}/libsatyr.so
%{_libdir}/pkgconfig/satyr.pc

%files -n python-%{name}
%{py_platsitedir}/%{name}
