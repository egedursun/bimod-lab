sudo systemctl daemon-reload
sudo mkdir -p /run/celery
sudo chown -R www-data:www-data /run/celery
sudo chmod -R 755 /run/celery
sudo chmod -R 755 /run/celery/celery-dev.pid
sudo chmod -R 755 /run/celery/celery-prod.pid

sudo systemctl restart celery_dev
sudo systemctl restart celery_prod

sudo systemctl start celerybeat_dev
sudo systemctl enable celerybeat_dev
