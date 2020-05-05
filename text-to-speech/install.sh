echo "Run this script with sudo if needed";


chmod u+x requirements.sh
chmod u+x build.sh

echo "Getting the required tools"
./requirements.sh

if [ $? -ne 0]; then
    echo "Failed at requirements.sh ...";
    exit 1;
fi

echo "Building..."
./build.sh

if [ $? -ne 0]; then
    echo "Failed at build.sh ...";
    exit 1;
fi

echo "Downloading a better voice..."
curl -O http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_aew.flitevox && mv cmu_us_aew.flitevox ./mimic1/voices/new_voice.flitevox;

if [ $? -ne 0]; then
    echo "Failed at downloading a voice file and moving it...";
    exit 1;
fi

echo "Running demo - if everything is okay, you should hear some text";
cd mimic1;

./mimic -t "Hello!" -voice ./voices/new_voice.flitevox

if [ $? -ne 0]; then
    echo "Failed at running the demo...";
    exit 1;
fi