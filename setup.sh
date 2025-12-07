#!/bin/bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-flask
pip3 install flask-cors --break-system-packages

sudo tee /etc/systemd/system/focusapp.service > /dev/null <<EOF
[Unit]
Description=Focus App
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/schedule-app
ExecStart=/usr/bin/python3 /home/pi/schedule-app/server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable focusapp
sudo systemctl start focusapp
pkill -f "python3 -m http.server 8080" 2>/dev/null || true

echo "Done! Access at http://raspberrypi.local:8080"
