sudo mkdir -p /var/www/bimod_dev/
sudo chown -R www-data:www-data /var/www/bimod_dev/
sudo chmod -R 755 /var/www/bimod_dev/
sudo systemctl daemon-reload

sudo systemctl start gunicorn_dev
sudo systemctl enable gunicorn_dev
