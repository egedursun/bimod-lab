#!/bin/bash

# Stop on any error
set -e

echo "          [Deploy / Production] Deployment started!"

echo "          [Deploy / Production] Checking for root privileges..."

# Define the directory
DEPLOY_DIR=/var/www/bimod_prod
REPO_URL=https://github.com/Bimod-HQ/bimod-lab.git
BRANCH=$1

echo "          [Deploy / Production] Root privileges checked!"

echo "          [Deploy / Production] Cloning or updating the repository..."

# Clone or update the repo
if [ ! -d "$DEPLOY_DIR" ]; then
  sudo git clone -b $BRANCH $REPO_URL $DEPLOY_DIR
else
  cd $DEPLOY_DIR
  git stash -u || true
  sudo git checkout main
  sudo git pull origin main
fi

echo "          [Deploy / Production] Repository cloned or updated!"

echo "          [Deploy / Production] Relocating to the directory..."

# Change to the directory
cd $DEPLOY_DIR

echo "          [Deploy / Production] Relocated to the directory!"

echo "          [Deploy / Production] Creating virtual environment..."

# Activate the virtual environment
source venv/bin/activate

echo "          [Deploy / Production] Virtual environment created!"

echo "Installing MariaDB development libraries.."
sudo apt install libmariadb-dev

echo "          [Deploy / Production] Installing requirements..."

# Install requirements
pip install -r requirements.txt

echo "          [Deploy / Production] Requirements installed!"

echo "Checking if py-solc-x is installed..."
pip3 show py-solc-x &> /dev/null

if [ $? -ne 0 ]; then
    echo "py-solc-x not found. Installing py-solc-x..."
    sudo pip3 install py-solc-x
else
    echo "py-solc-x is already installed."
fi

echo "Installing Solidity compiler version 0.8.0..."
python3 << EOF
import solcx
solcx.install_solc('0.8.0')
EOF

echo "          [Deploy / Production] Solidity compiler version 0.8.0 installed."

echo "          [Deploy / Production] SolCX Solidity Compiler installed!"

echo "          [Deploy / Production] Running database migrations..."

# Database migrations
python3 manage.py migrate

echo "          [Deploy / Production] Database migrations completed!"

echo "          [Deploy / Production] Collecting static files..."

# Collect static files
python3 manage.py collectstatic --noinput

echo "          [Deploy / Production] Static files collected!"

echo "          [Deploy / Production] Restarting services..."

if ! sudo systemctl is-active --quiet redis; then
    echo "          [Deploy / Production] Redis is not active. Starting Redis..."
    sudo systemctl start redis
    echo "          [Deploy / Production] Redis started!"
fi

echo "          [Deploy / Production] Granting permissions..."

# Restart services
sudo mkdir -p /run/uvicorn/
sudo chown www-data:www-data /run/uvicorn/
sudo chmod 755 /run/uvicorn/
sudo mkdir -p /run/celery
sudo chown www-data:www-data /run/celery
sudo chown www-data:www-data /var/www/bimod_dev/apps/core/generative_ai/tmp
sudo chmod 755 /run/celery

echo "          [Deploy / Production] Restarting services..."

systemctl daemon-reload

echo "          [Deploy / Production] Reloaded daemon!"

sudo systemctl restart redis

echo "          [Deploy / Production] Restarted Redis!"

sudo systemctl restart gunicorn_prod

echo "          [Deploy / Production] Restarted Gunicorn!"

sudo systemctl restart nginx

echo "          [Deploy / Production] Restarted Nginx!"

set +e
sudo systemctl restart celery_prod
set -e

echo "          [Deploy / Production] Restarted Celery!"

sudo systemctl restart celerybeat_prod

echo "          [Deploy / Production] Restarted Celery Beat!"

sudo systemctl restart flower_prod

echo "          [Deploy / Production] Restarted Flower!"

echo "[Production / Deploy] Deployment successful!"

# Run the integration tests
pytest

echo "[Production / Deploy] Integration tests are completed successfully!"

echo "[Production / Deploy] Deployment completed successfully!"
