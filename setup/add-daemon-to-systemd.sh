#!/bin/bash

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
