
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
    

    





