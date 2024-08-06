#!/bin/bash

# Stop on any error
set -e

# Define the directory
DEPLOY_DIR=/var/www/bimod_dev
REPO_URL=https://github.com/Bimod-HQ/bimod-app.git
BRANCH=$1

# Clone or update the repo
if [ ! -d "$DEPLOY_DIR" ]; then
  sudo git clone -b $BRANCH $REPO_URL $DEPLOY_DIR
else
  cd $DEPLOY_DIR
  git stash -u || true
  sudo git checkout dev
  sudo git pull origin dev
fi

# Change to the directory
cd $DEPLOY_DIR

# Activate the virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Database migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

if ! sudo systemctl is-active --quiet redis; then
    echo "[Deploy / Development] Redis is not active. Starting Redis..."
    sudo systemctl start redis
fi

# Restart services
sudo mkdir -p /run/celery
sudo chown www-data:www-data /run/celery
sudo chmod 755 /run/celery

systemctl daemon-reload
sudo systemctl restart redis
sudo systemctl restart gunicorn_dev
sudo systemctl restart nginx
sudo systemctl restart celery_dev
sudo systemctl restart celerybeat_dev
sudo systemctl restart flower_dev

echo "[Deploy / Development] Deployment successful!"
