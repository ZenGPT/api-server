ssh ubuntu@3.215.107.112 << EOF
sudo tail -n 100 /var/log/supervisor/api-server-stdout---supervisor-*.log
EOF
