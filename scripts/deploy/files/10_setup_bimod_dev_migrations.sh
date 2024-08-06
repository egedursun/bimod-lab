cd /var/www/bimod_dev
source venv/bin/activate
python3 manage.py migrate
python3 manage.py collectstatic
deactivate
