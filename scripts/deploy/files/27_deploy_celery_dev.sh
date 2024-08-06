sudo mkdir -p /run/celery
sudo chown www-data:www-data /run/celery
systemctl daemon-reload
sudo systemctl restart celery_dev
sudo systemctl start celery_dev
sudo systemctl enable celery_dev
