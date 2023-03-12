ssh ubuntu@ai.gptdock.com << EOF
cd api-server
git pull
sudo pip3 install -r requirements.txt
sudo supervisorctl restart all
EOF
