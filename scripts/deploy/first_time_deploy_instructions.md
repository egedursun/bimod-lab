
**Steps to Set Up the Remote Server**

1. SSH into the remote server.

    ```bash
    ssh root@185.170.198.44
    ```

2. Update the package list and upgrade the packages.

    ```bash
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
    cd /var/www/bimod_dev/bimod-app
    sudo apt install python3-venv
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
    
    cd ../bimod_prod/bimod-app
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
    cd /var/www/bimod_dev/bimod-app
    touch .env
    nano .env
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
    WorkingDirectory=/var/www/bimod_dev/bimod-app
    ExecStart=/var/www/bimod_dev/bimod-app/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/bimod_dev/bimod-app/gunicorn.sock config.wsgi:application
    
    [Install]
    WantedBy=multi-user.target
    ```
    
    Enable and start the Gunicorn service.

    ```bash
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
    
      location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
          root /var/www/bimod_dev/bimod-app;
        }
        location /media/ {
            root /var/www/bimod_dev/bimod-app;
        }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/bimod_dev/bimod-app/gunicorn.sock;
    }

    listen [::]:443 ssl ipv6only=on;
    listen 443 ssl; 
    ssl_certificate /etc/letsencrypt/live/bimod.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bimod.io/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    if ($scheme != "https") {
        return 301 https://$host$request_uri;
      } # managed by Certbot
    }
    ```
    
    Save and exit the file.

    ```bash
    sudo ln -s /etc/nginx/sites-available/bimod.io /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```
    
14. Set Up the Logging Directory

    ```bash
    sudo mkdir /var/log/bimod_dev
    sudo touch /var/log/bimod_dev/django_debug.log
    sudo chown www-data:www-data /var/log/bimod_dev/django_debug.log
    sudo chmod 644 /var/log/bimod_dev/django_debug.log
    
    sudo mkdir /var/log/bimod_prod
    sudo touch /var/log/bimod_prod/django_debug.log
    sudo chown www-data:www-data /var/log/bimod_prod/django_debug.log
    sudo chmod 644 /var/log/bimod_prod/django_debug.log
    ```

    
15. Setting up Celery.

    ```bash
    sudo nano /etc/systemd/system/celery.service
    ```
    
    Add the following lines to the file.

    ```text
      [Unit]
      Description=Celery Service
      After=network.target
    
      [Service]
      Type=forking
      User=www-data
      Group=www-data
      WorkingDirectory=/var/www/bimod_dev/bimod-app
      ExecStart=/usr/local/bin/celery -A config worker --loglevel=info
    
      [Install]
      WantedBy=multi-user.target
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
    Type=forking
    User=www-data
    Group=www-data
    WorkingDirectory=/var/www/bimod_dev/bimod-app
    ExecStart=/usr/local/bin/celery -A config beat --loglevel=info
    
    [Install]
    WantedBy=multi-user.target
    ```
    
16. Enable and start the Celery services.

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl restart celery
    sudo systemctl start celery
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
    WorkingDirectory=/var/www/bimod_dev/bimod-app
    ExecStart=/var/www/bimod_dev/bimod-app/venv/bin/flower --port=5555 --broker=redis://localhost:6379/0
    Restart=always
    
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
    


    
