VERSION=0.8.1

if [ ! -d libjxl ]; then
git clone https://github.com/libjxl/libjxl
fi
cd libjxl/
git checkout .
git checkout v${VERSION}
git submodule init ; git submodule update
git pull
rm -r third_party/brotli/ third_party/googletest/
rm -r third_party/HEVCSoftware/ third_party/highway/
rm -r third_party/lcms/ third_party/libpng/
rm -r third_party/skcms/profiles/ third_party/zlib
tar -zcvf ../third_party-${VERSION}.tar.gz third_party/
