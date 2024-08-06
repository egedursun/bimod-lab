sudo mkdir -p /run/celery
sudo chown www-data:www-data /run/celery
systemctl daemon-reload
sudo systemctl restart celery_prod
sudo systemctl start celery_prod
sudo systemctl enable celery_prod
