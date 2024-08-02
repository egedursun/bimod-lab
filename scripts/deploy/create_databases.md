
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
    CREATE USER admin_prod WITH PASSWORD 'XRUs1Cz3Dxiwb6e';
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
    git clone https://egedursun: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@github.com/Bimod-HQ/bimod-app.git
       # Username: egedursun
       # Password: ***
    cd bimod-app


