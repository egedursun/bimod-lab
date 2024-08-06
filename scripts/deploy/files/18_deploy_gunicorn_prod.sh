sudo mkdir -p /var/www/bimod_prod/
sudo chown -R www-data:www-data /var/www/bimod_prod/
sudo chmod -R 755 /var/www/bimod_prod/
sudo systemctl daemon-reload

sudo systemctl start gunicorn_prod
sudo systemctl enable gunicorn_prod
