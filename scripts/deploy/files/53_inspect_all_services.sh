sudo systemctl status gunicorn_dev
sudo journalctl -xeu gunicorn_dev

sudo systemctl status gunicorn_prod
sudo journalctl -xeu gunicorn_prod

###

sudo systemctl status celery_dev
sudo journalctl -xeu celery_dev

sudo systemctl status celery_prod
sudo journalctl -xeu celery_prod

###

sudo systemctl status celerybeat_dev
sudo journalctl -xeu celerybeat_dev

sudo systemctl status celerybeat_prod
sudo journalctl -xeu celerybeat_prod

###

sudo systemctl status flower_dev
sudo journalctl -xeu flower_dev

sudo systemctl status flower_prod
sudo journalctl -xeu flower_prod

###

sudo systemctl status redis-server
sudo journalctl -xeu redis-server

###

sudo systemctl status nginx
sudo journalctl -xeu nginx
