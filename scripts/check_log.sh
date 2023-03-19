ssh ubuntu@3.215.107.112 << EOF
sudo tail -n 100 /var/log/supervisor/gptdock-stdout---supervisor-*.log
EOF
