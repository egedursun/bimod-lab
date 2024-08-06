sudo systemctl start gunicorn_dev
sudo systemctl start gunicorn_prod

sudo systemctl start celery_dev
sudo systemctl start celery_prod

sudo systemctl start celerybeat_dev
sudo systemctl start celerybeat_prod

sudo systemctl start flower_dev
sudo systemctl start flower_prod

sudo systemctl start redis-server
sudo systemctl start nginx
