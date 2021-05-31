%global gdk_pixbuf_moduledir $(pkgconf gdk-pixbuf-2.0 --variable=gdk_pixbuf_moduledir)

%global name_dash jpeg-xl

# https://github.com/libjxl/libjxl/issues/63
# https://github.com/libjxl/libjxl/issues/64
%global toolchain clang

# https://bugzilla.redhat.com/show_bug.cgi?id=1918924
%ifarch %arm32
%global _lto_cflags %{nil}
%endif

%global common_description %{expand:
This package contains a reference implementation of JPEG XL (encoder and
decoder). As previously announced, it is available under a royalty-free and open
source license (Apache 2).}

Name:           jpegxl
Version:        0.3.7
%global commit  9e9bce86164dc4d01c39eeeb3404d6aed85137b2
Release:        2%{?dist}
Summary:        JPEG XL image format reference implementation

# Main library: ASL 2.0
# lodepng: zlib
# sjpeg: ASL 2.0
# skcms: BSD
License:        ASL 2.0 and zlib and BSD
URL:            https://jpeg.org/jpegxl/
VCS:            https://gitlab.com/wg1/jpeg-xl
Source0:        %vcs/-/archive/v%{version}/%{name_dash}-%{version}.tar.bz2

# git clone https://gitlab.com/wg1/jpeg-xl.git
# cd jpeg-xl/
# git checkout v%%{version}
# git submodule init ; git submodule update
# rm -r third_party/brotli/ third_party/difftest_ng/ third_party/googletest/
# rm -r third_party/HEVCSoftware/ third_party/highway/
# rm -r third_party/IQA-optimization/ third_party/lcms/
# rm -r third_party/skcms/profiles/ third_party/vmaf/ third_party/testdata/
# tar -zcvf third_party-%%{version}.tar.gz third_party/
Source1:        third_party-%{version}.tar.gz

BuildRequires:  asciidoc
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  extra-cmake-modules
BuildRequires:  clang
BuildRequires:  giflib-devel
BuildRequires:  gperftools-devel
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(gimp-2.0)
BuildRequires:  (pkgconfig(glut) or pkgconfig(freeglut))
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(libhwy)
BuildRequires:  pkgconfig(libbrotlicommon)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(zlib)

# Header-only library to be directly included in the project's source tree
Provides:       bundled(lodepng) = 0-0.1.20210522git48e5364
# No official release
Provides:       bundled(sjpeg) = 0-0.1.20210522git868ab55
# Build system is Bazel, which is not packaged by Fedora
Provides:       bundled(skcms) = 0-0.1.20210522git6437475

%description
%common_description

%package        utils
Summary:        JPEG XL image format reference implementation
Recommends:     jxl-pixbuf-loader = %{version}-%{release}
Recommends:     gimp-jxl-plugin   = %{version}-%{release}

%description utils
%{common_description}

%package        doc
Summary:        Documentation for JPEG-XL
BuildArch:      noarch

%description    doc
%{common_description}

Documentation for JPEG-XL.

%package        libs
Summary:        Library files for JPEG-XL
Requires:       shared-mime-info
Recommends:     jxl-pixbuf-loader = %{version}-%{release}
Recommends:     gimp-jxl-plugin   = %{version}-%{release}

%description    libs
%{common_description}

Library files for JPEG-XL.

%package        devel
Summary:        Development files for JPEG-XL
Requires:       jpegxl-libs%{?_isa} = %{version}-%{release}

%description    devel
%{common_description}

Development files for JPEG-XL.

%package     -n jxl-pixbuf-loader
Summary:        JPEG-XL image loader for GTK+ applications
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
Requires:       gdk-pixbuf2

%description -n jxl-pixbuf-loader
Jxl-pixbuf-loader contains a plugin to load JPEG-XL images in GTK+ applications.

%package     -n gimp-jxl-plugin
Summary:        A plugin for loading and saving JPEG-XL images
Requires:       gimp

%description -n gimp-jxl-plugin
This is a GIMP plugin for loading and saving JPEG-XL images.

%prep
%autosetup -p1 -n %{name_dash}-v%{version}-%{commit}
rm -rf third_party/
%setup -q -T -D -a 1 -n %{name_dash}-v%{version}-%{commit}

%build
%cmake  -DENABLE_CCACHE=1 \
        -DBUILD_TESTING=OFF \
        -DINSTALL_GTEST:BOOL=OFF \
        -DJPEGXL_ENABLE_BENCHMARK:BOOL=OFF \
        -DJPEGXL_ENABLE_PLUGINS:BOOL=ON \
        -DJPEGXL_FORCE_SYSTEM_BROTLI:BOOL=ON \
        -DJPEGXL_FORCE_SYSTEM_GTEST:BOOL=ON \
        -DJPEGXL_FORCE_SYSTEM_HWY:BOOL=ON \
        -DJPEGXL_WARNINGS_AS_ERRORS:BOOL=OFF \
        -DBUILD_SHARED_LIBS:BOOL=OFF
%cmake_build -- all doc

%install
%cmake_install
rm -v %{buildroot}%{_libdir}/*.a

%files utils
%doc CONTRIBUTING.md CONTRIBUTORS README.md
%{_bindir}/cjxl
%{_bindir}/djxl
%{_mandir}/man1/cjxl.1*
%{_mandir}/man1/djxl.1*

%files doc
%doc doc/*.md
%doc %{_vpath_builddir}/html
%license LICENSE

%files libs
%license LICENSE
%{_libdir}/libjxl.so.0*
%{_libdir}/libjxl_threads.so.0*
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/jxl.thumbnailer
%{_datadir}/mime/packages/image-jxl.xml

%files devel
%doc CONTRIBUTING.md
%{_includedir}/jxl/
%{_libdir}/libjxl.so
%{_libdir}/libjxl_threads.so
%{_libdir}/pkgconfig/libjxl.pc
%{_libdir}/pkgconfig/libjxl_threads.pc

%files -n jxl-pixbuf-loader
%license LICENSE
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-jxl.so

%files -n gimp-jxl-plugin
%license LICENSE
%{_libdir}/gimp/2.0/plug-ins/file-jxl/

%changelog
* Mon May 31 21:07:22 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.7-2
- Use Clang instead of GCC due to vector conversion strictness of GCC
- Disable LTO on arm due to Clang 12.0.0 bug
- Close: rhbz#1922638

* Mon May 17 20:49:39 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.7-1
- Update to 0.3.7

* Sat Jan 30 17:10:24 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3-1
- Update to 0.3

* Sat Dec 12 03:45:24 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.1.1-1
- Update to 0.1.1

* Wed Jul 15 17:00:49 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.0.1-0.1.20200715git0a46d01c
- Initial RPM
