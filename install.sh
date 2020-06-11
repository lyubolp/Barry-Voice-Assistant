echo "Starting daemon"
./add-daemon-to-systemd.sh

echo "Installing actions..."
./install_actions.sh
echo "Done !"

echo "Installing the text-to-speech actions..."
cd text-to-speech
./install.sh

echo "Done !"

cd ..
