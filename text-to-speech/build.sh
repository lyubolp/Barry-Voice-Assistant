git clone https://github.com/MycroftAI/mimic1.git
cd mimic1
./dependencies.sh --prefix="/usr/local"
./autogen.sh
./configure --prefix="/usr/local" --disable-lang-indic
make
make check
