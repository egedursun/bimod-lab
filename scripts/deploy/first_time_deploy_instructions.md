
**Steps to Set Up the Remote Server**

1. SSH into the remote server.

    ```bash
    ssh root@185.170.198.44
    ```
2. Update the package list and upgrade the packages.

    ```bash
    cd /root/var/www
    sudo apt update
    sudo apt upgrade
    ```
3. Install the necessary packages for the project.

    ```bash
   sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
    ```
4. Connect to the PostgreSQL database.

    ```bash
    sudo -u postgres psql
   ```
5. Create a new database for the project.

    ```sql
    CREATE DATABASE bimod_dev;
    CREATE USER admin_dev WITH PASSWORD '***';
    ALTER ROLE admin_dev SET client_encoding TO 'utf8';
    ALTER ROLE admin_dev SET default_transaction_isolation TO 'read committed';
    ALTER ROLE admin_dev SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE bimod_dev TO admin_dev;
  
    CREATE DATABASE bimod_prod;
    CREATE USER admin_prod WITH PASSWORD '***';
    ALTER ROLE admin_prod SET client_encoding TO 'utf8';
    ALTER ROLE admin_prod SET default_transaction_isolation TO 'read committed';
    ALTER ROLE admin_prod SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE bimod_prod TO admin_prod;
    ```
6. Exit the PSQL.

    ```sql
    \q
    ```
7. Exit PostgreSQL.

    ```bash
    exit
    ```
8. Setting up the project folders.

    ```bash
    cd /var/www
    sudo mkdir bimod_dev
    sudo mkdir bimod_prod
    sudo chown -R root:www-data bimod_dev
    sudo chown -R root:www-data bimod_prod
    sudo chmod o+x /root
   ```
9. Clone the project repository.

    ```bash
    cd bimod_dev
    git clone -b dev https://egedursun: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@github.com/Bimod-HQ/bimod-app.git
    cd ..
    
    cd bimod_prod
    git clone -b main https://egedursun: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@github.com/Bimod-HQ/bimod-app.git
    cd ..
    ```
10. Setting up the virtual environment.

    ```bash
    cd /root/var/www/bimod_dev/bimod-app
    sudo apt install python3-venv
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
    
    cd /root/var/www/bimod_prod/bimod-app
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
    cd ../..
    ```
11. Allow Postgres to listen to your local machine:

    ```bash
    sudo nano /etc/postgresql/14/main/pg_hba.conf
    ```
    
    Add the following line to the file:
    
    ```text
    host    all             all             0.0.0.0/0            md5
    ```
    
    Save and exit the file.

    ```bash
    sudo nano /etc/postgresql/14/main/postgresql.conf
    ```
    
    Find the line that says `#listen_addresses = 'localhost'` and change it to `listen_addresses = '*'`.

    Save and exit the file.

    Adjust the firewall settings:

    ```bash
    sudo ufw allow 5432/tcp
    sudo ufw reload
    ```
    
    Restart the PostgreSQL service:

    ```bash
    sudo systemctl restart postgresql
    ``` 
12. Setting up the environment variables.

    ```bash
    cd /root/var/www/bimod_dev/bimod-app
    touch .env
    nano .env
    touch .env.prod
    nano .env.prod
    
    cd /root/var/www/bimod_prod/bimod-app
    touch .env
    nano .env
    touch .env.prod
    nano .env.prod
    ```
    
    Add the environment variables to the `.env` file.

    ```text
    ***
    ```
    
    Save and exit the file.

    ```bash
    cd /var/www/bimod_dev/bimod-app
    source venv/bin/activate
    python3 manage.py migrate
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic
    deactivate
    
    cd /var/www/bimod_prod/bimod-app
    source venv/bin/activate
    python3 manage.py migrate
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic
    deactivate
    ``` 
13. Setting up the Gunicorn service.

    ```bash
    sudo nano /etc/systemd/system/gunicorn.service
    ```
    
    Add the following lines to the file.

    ```text
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/root/var/www/bimod_dev/bimod-app
Environment="PATH=/root/var/www/bimod_dev/bimod-app/venv/bin"
ExecStart=/root/var/www/bimod_dev/bimod-app/venv/bin/gunicorn --access-logfile - --error-logfile - --log-level debug --workers 3 --bind unix:/root/var/www/bimod_dev/bimod-app/gunicorn.sock config.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

    ```
    
    Enable and start the Gunicorn service.

    ```bash
    sudo mkdir -p /root/var/www/bimod_dev/bimod-app/
    sudo chown -R www-data:www-data /root/var/www/bimod_dev/bimod-app/
    sudo chmod -R 755 /root/var/www/bimod_dev/bimod-app/
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    ```
14. Setting up the Nginx server.

    ```bash
    sudo nano /etc/nginx/sites-available/bimod.io
    ```
    
    Add the following lines to the file.

    ```text
server {
    listen 80;
    server_name bimod.io www.bimod.io;

    location = /favicon.ico {
        alias /src/assets/img/favicon/favicon.ico;
        access_log off;
        log_not_found off;
    }
    location /static/ {
        alias /root/var/www/bimod_dev/bimod-app/staticfiles/;
    }
    location /media/ {
        alias /root/var/www/bimod_dev/bimod-app/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/root/var/www/bimod_dev/bimod-app/gunicorn.sock;
    }

    # Redirect HTTP to HTTPS
    if ($scheme != "https") {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name bimod.io www.bimod.io;

    ssl_certificate /etc/letsencrypt/live/bimod.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bimod.io/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /root/var/www/bimod_dev/bimod-app/staticfiles/;
    }
    location /media/ {
        alias /root/var/www/bimod_dev/bimod-app/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/root/var/www/bimod_dev/bimod-app/gunicorn.sock;
    }
}
    ```
    
    Save and exit the file.

    ```bash
    sudo ln -s /etc/nginx/sites-available/bimod.io /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

    
14. Setting up Celery.

    ```bash
    sudo nano /etc/systemd/system/celery.service
    ```
    
    Add the following lines to the file.

    ```service
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/root/var/www/bimod_dev/bimod-app
ExecStart=/bin/bash -c 'source /root/var/www/bimod_dev/bimod-app/venv/bin/activate && celery -A config worker --loglevel=info --detach --pidfile=/run/celery/celery.pid'
ExecStartPost=/bin/sleep 5
PIDFile=/run/celery/celery.pid
Restart=always
RestartSec=5
StartLimitInterval=60
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
    ```

    Enable and start the Celery service.

    ```bash
    sudo mkdir -p /run/celery
    sudo chown www-data:www-data /run/celery
    systemctl daemon-reload
    sudo systemctl restart celery
    sudo systemctl start celery
    sudo systemctl enable celery

    sudo systemctl status celery
    ```

15. Setting up Celery Beat.

    ```bash
    sudo nano /etc/systemd/system/celerybeat.service
    ```
    
    Add the following lines to the file.

    ```text
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/root/var/www/bimod_dev/bimod-app
ExecStart=/bin/bash -c 'source /root/var/www/bimod_dev/bimod-app/venv/bin/activate && exec celery -A config beat --loglevel=info'
Restart=always

[Install]
WantedBy=multi-user.target
    ```
    
16. Enable and start the Celery services.

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl restart celery
    sudo systemctl enable celery
    sudo systemctl start celerybeat
    sudo systemctl enable celerybeat
    
    sudo systemctl status celery
    sudo systemctl status celerybeat
    ```
    
17. Setting up the Flower service.

    ```bash
    sudo nano /etc/systemd/system/flower.service
    ```
    
    Add the following lines to the file.

    ```text
[Unit]
Description=Flower Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/root/var/www/bimod_dev/bimod-app
ExecStart=/bin/bash -c 'source /root/var/www/bimod_dev/bimod-app/venv/bin/activate && exec celery -A config flower --port=5555 --broker=redis://localhost:6379/0'
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
    ```
    
    Enable and start the Flower service.

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl restart flower
    sudo systemctl start flower
    sudo systemctl enable flower
    
    sudo systemctl status flower
    ```
    
    Update the firewall settings.

    ```bash
    sudo ufw allow 5555
    sudo ufw reload
    ```

    
18. Setting up the Redis service.

    ```bash
    sudo apt update
    sudo apt install redis-server
    sudo nano /etc/redis/redis.conf
    ```
    
    Find the line that says `supervised no` and change it to `supervised systemd`.

    Save and exit the file.

    ```bash
    sudo systemctl restart redis-server
    sudo systemctl enable redis-server
    
    sudo systemctl status redis-server
    ```
    
19. Setting up the start up script.

    ```bash
    sudo nano /etc/rc.local
    ```
    
    Add the following lines to the file.

    ```text
    #!/bin/bash
    sudo systemctl start gunicorn
    sudo systemctl start celery
    sudo systemctl start celerybeat
    sudo systemctl start flower
    sudo systemctl start redis-server
    exit 0
    ```
    
    Save and exit the file.

    ```bash
    
    ```

20. Run the server

    ```bash
    sudo systemctl start gunicorn
    sudo systemctl start celery
    sudo systemctl start celerybeat
    sudo systemctl start flower
    sudo systemctl start redis-server
    sudo systemctl start nginx
    ```
