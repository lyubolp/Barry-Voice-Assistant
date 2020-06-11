#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "Daemon initialization must be done as root"
    exit 1
fi

projectRoot="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd ))"

cat > "/etc/systemd/system/barry.service" << EOF
[Unit]
Description=Barry speech recognition

[Service]
Type=forking
User=root
ExecStart=${projectRoot}/daemon/barryd.py start

[Install]
WantedBy=multi-user.target
EOF

systemctl enable barry
systemctl start barry
