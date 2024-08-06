cd /var/www/bimod_prod
source venv/bin/activate
python3 manage.py migrate
python3 manage.py collectstatic
deactivate
