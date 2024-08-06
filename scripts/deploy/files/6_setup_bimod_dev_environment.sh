cd /var/www/bimod_dev
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate
