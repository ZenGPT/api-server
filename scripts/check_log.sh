ssh ubuntu@ai.gptdock.com << EOF
sudo tail -n 100 /var/log/supervisor/api-server-stdout---supervisor-*.log
EOF
