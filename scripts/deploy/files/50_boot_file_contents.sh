sudo systemctl start gunicorn
sudo systemctl start celery
sudo systemctl start celerybeat
sudo systemctl start flower
sudo systemctl start redis-server
exit 0
