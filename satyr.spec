%define _disable_ld_no_undefined 1

# rhel6's python-sphinx cannot build manual pages
%if 0
  %define enable_python_manpage 0
%else
  %define enable_python_manpage 1
%endif

%define major 3
%define libname %mklibname %{name} %{major}

Name: satyr
Version: 0.15
Release: 3
Summary: Tools to create anonymous, machine-friendly problem reports
Group: System/Libraries
License: GPLv2+
URL: https://github.com/abrt/satyr
Source0: https://fedorahosted.org/released/abrt/satyr-%{version}.tar.xz
Patch1:	satyr-0.15-rpm5.patch
BuildRequires: python2-devel
BuildRequires: elfutils-devel
BuildRequires: binutils-devel
BuildRequires: rpm-devel
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: gcc-c++
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

%package -n python2-%{name}
Summary: Python bindings for %{name}
Group: Development/Python
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python2-%{name}
Python bindings for %{name}.

%prep
%setup -q
%apply_patches
sed -i 's/env python/env python2/' tests/python/*.py

printf '%s' '%{version}' > satyr-version
autoreconf -fiv

%build
export PYTHON=python2
%configure \
%if ! %{?enable_python_manpage}
        --disable-python-manpage 
%endif

%make V=1

%install
make install DESTDIR=%{buildroot}

# Remove all libtool archives (*.la) from modules directory.
find %{buildroot} -name "*.la" | xargs rm --

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README NEWS COPYING
%{_bindir}/satyr
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%{_libdir}/libsatyr.so.%{major}*
%files devel
%{_includedir}/satyr/
%{_libdir}/libsatyr.so
%{_libdir}/pkgconfig/satyr.pc

%files -n python2-%{name}
%{py2_platsitedir}/%{name}

%if %{?enable_python_manpage}
%{_mandir}/man3/satyr-python.3*
%endif


