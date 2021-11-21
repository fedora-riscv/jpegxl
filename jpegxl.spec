%global gdk_pixbuf_moduledir $(pkgconf gdk-pixbuf-2.0 --variable=gdk_pixbuf_moduledir)

# https://github.com/libjxl/libjxl/issues/63
# %%global toolchain clang

%global common_description %{expand:
This package contains a reference implementation of JPEG XL (encoder and
decoder).}

Name:           jpegxl
Version:        0.6.1
Release:        %autorelease
Summary:        JPEG XL image format reference implementation

# Main library: BSD
# lodepng: zlib
# sjpeg: ASL 2.0
# skcms: BSD
License:        BSD and ASL 2.0 and zlib
URL:            https://jpeg.org/jpegxl/
VCS:            https://github.com/libjxl/libjxl
Source0:        %vcs/archive/v%{version}/%{name}-%{version}.tar.gz

# git clone https://github.com/libjxl/libjxl
# cd libjxl/
# git checkout v%%{version}
# git submodule init ; git submodule update
# rm -r third_party/brotli/ third_party/difftest_ng/ third_party/googletest/
# rm -r third_party/HEVCSoftware/ third_party/highway/
# rm -r third_party/IQA-optimization/ third_party/lcms/
# rm -r third_party/skcms/profiles/ third_party/vmaf/ third_party/testdata/
# tar -zcvf ../third_party-%%{version}.tar.gz third_party/
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
BuildRequires:  gtest-devel
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

%package     -n libjxl-utils
Summary:        Utilities for manipulating JPEG XL images
Recommends:     jxl-pixbuf-loader = %{version}-%{release}
Recommends:     gimp-jxl-plugin   = %{version}-%{release}
Provides:       jpegxl-utils = %{version}-%{release}
Obsoletes:      jpegxl-utils < 0.3.7-5

%description -n libjxl-utils
%{common_description}

%package        doc
Summary:        Documentation for JPEG-XL
BuildArch:      noarch

%description    doc
%{common_description}

Documentation for JPEG-XL.

%package     -n libjxl
Summary:        Library files for JPEG-XL
Requires:       shared-mime-info
Recommends:     jxl-pixbuf-loader = %{version}-%{release}
Provides:       jpegxl-libs = %{version}-%{release}
Obsoletes:      jpegxl-libs < 0.3.7-5

%description -n libjxl
%{common_description}

Library files for JPEG-XL.

%package     -n libjxl-devel
Summary:        Development files for JPEG-XL
Requires:       libjxl%{?_isa} = %{version}-%{release}
Provides:       jpegxl-devel = %{version}-%{release}
Obsoletes:      jpegxl-devel < 0.3.7-5

%description -n libjxl-devel
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
%autosetup -p1 -n libjxl-%{version}
rm -rf third_party/
%setup -q -T -D -a 1 -n libjxl-%{version}

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

%files -n libjxl-utils
%doc CONTRIBUTING.md CONTRIBUTORS README.md
%{_bindir}/cjxl
%{_bindir}/djxl
%{_mandir}/man1/cjxl.1*
%{_mandir}/man1/djxl.1*

%files doc
%doc doc/*.md
%doc %{_vpath_builddir}/html
%license LICENSE

%files -n libjxl
%license LICENSE
%{_libdir}/libjxl.so.0*
%{_libdir}/libjxl_threads.so.0*
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/jxl.thumbnailer
%{_datadir}/mime/packages/image-jxl.xml

%files -n libjxl-devel
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
%autochangelog
