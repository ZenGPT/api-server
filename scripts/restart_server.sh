ssh ubuntu@3.215.107.112 << EOF
cd api-server
git pull
sudo pip3 install -r requirements.txt
sudo supervisorctl restart all
EOF
