Summary:	PNG encoder and decoder in C and C++, without dependencies
Summary(pl.UTF-8):	Koder i dekoder PNG w C i C++ bez zależności
Name:		lodepng
%define	snap	20200306
%define	gitref	e34ac04553e51a6982ae234d98ce6b76dd57a6a1
%define	rel	1
Version:	0
Release:	0.%{snap}.%{rel}
License:	BSD-like + altered sources must be marked
Group:		Libraries
Source0:	https://github.com/lvandeve/lodepng/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	4557f32be35a404d20f5fcc784fe48c5
Patch0:		%{name}-c.patch
URL:		http://lodev.org/lodepng/
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PNG encoder and decoder in C and C++, without dependencies.

%description -l pl.UTF-8
Koder i dekoder PNG w C i C++ bez zależności.

%package devel
Summary:	Header files for lodepng library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lodepng
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for lodepng library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lodepng.

%package static
Summary:	Static lodepng library
Summary(pl.UTF-8):	Statyczna biblioteka lodepng
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lodepng library.

%description static -l pl.UTF-8
Statyczna biblioteka lodepng.

%prep
%setup -q -n %{name}-%{gitref}
%patch -P0 -p1

%build
libtool --tag=CXX --mode=compile %{__cxx} %{rpmcxxflags} %{rpmcppflags} -o lodepng.lo -c lodepng.cpp
libtool --tag=CXX --mode=compile %{__cxx} %{rpmcxxflags} %{rpmcppflags} -o lodepng_util.lo -c lodepng_util.cpp
libtool --tag=CXX --mode=link %{__cxx} %{rpmldflags} %{rpmcxxflags} -o liblodepng.la lodepng.lo -rpath %{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_examplesdir}/%{name}-%{version}}

libtool --mode=install install liblodepng.la $RPM_BUILD_ROOT%{_libdir}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblodepng.la

cp -p lodepng.h lodepng_util.h $RPM_BUILD_ROOT%{_includedir}

cp -p examples/*.{c,cpp} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/liblodepng.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblodepng.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblodepng.so
%{_includedir}/lodepng.h
%{_includedir}/lodepng_util.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/liblodepng.a
