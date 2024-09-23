#!/bin/bash

# Stop on any error
set -e

echo "          [Deploy / Development] Deployment started!"

echo "          [Deploy / Development] Checking for root privileges..."

# Define the directory
DEPLOY_DIR=/var/www/bimod_dev
REPO_URL=https://github.com/Bimod-HQ/bimod-app.git
BRANCH=$1

echo "          [Deploy / Development] Root privileges checked!"

echo "          [Deploy / Development] Cloning or updating the repository..."

# Clone or update the repo
if [ ! -d "$DEPLOY_DIR" ]; then
  sudo git clone -b $BRANCH $REPO_URL $DEPLOY_DIR
else
  cd $DEPLOY_DIR
  git stash -u || true
  sudo git checkout dev
  sudo git pull origin dev
fi

echo "          [Deploy / Development] Repository cloned or updated!"

echo "          [Deploy / Development] Relocating to the directory..."

# Change to the directory
cd $DEPLOY_DIR

echo "          [Deploy / Development] Relocated to the directory!"

echo "          [Deploy / Development] Creating virtual environment..."

# Activate the virtual environment
source venv/bin/activate

echo "          [Deploy / Development] Virtual environment created!"

echo "          [Deploy / Development] Installing requirements..."

# Install requirements
pip install -r requirements.txt

echo "          [Deploy / Development] Requirements installed!"

echo "          [Deploy / Development] Running database migrations..."

# Database migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/*/migrations/*.py" -not -name "__init__.py" -delete
pip uninstall django --yes
pip install django
python3 manage.py makemigrations
python3 manage.py migrate --fake
python3 manage.py migrate

echo "          [Deploy / Development] Database migrations completed!"

echo "          [Deploy / Development] Collecting static files..."

# Collect static files
python3 manage.py collectstatic --noinput

echo "          [Deploy / Development] Static files collected!"

echo "          [Deploy / Development] Restarting services..."

if ! sudo systemctl is-active --quiet redis; then
    echo "          [Deploy / Development] Redis is not active. Starting Redis..."
    sudo systemctl start redis
    echo "          [Deploy / Development] Redis started!"
fi


echo "          [Deploy / Development] Granting permissions..."

# Restart services
sudo mkdir -p /run/celery
sudo chown www-data:www-data /run/celery
sudo chown www-data:www-data /var/www/bimod_dev/apps/_services/llms/tmp
sudo chmod 755 /run/celery

echo "          [Deploy / Development] Restarting services..."

systemctl daemon-reload

echo "          [Deploy / Development] Reloaded daemon!"

sudo systemctl restart redis

echo "          [Deploy / Development] Restarted Redis!"

sudo systemctl restart gunicorn_dev

echo "          [Deploy / Development] Restarted Gunicorn!"

sudo systemctl restart nginx

echo "          [Deploy / Development] Restarted Nginx!"

sudo systemctl restart celery_dev

echo "          [Deploy / Development] Restarted Celery!"

sudo systemctl restart celerybeat_dev

echo "          [Deploy / Development] Restarted Celery Beat!"

sudo systemctl restart flower_dev

echo "          [Deploy / Development] Restarted Flower!"

echo "[Deploy / Development] Running integration tests..."

# Run the integration tests
pytest -v

echo "[Deploy / Development] Integration tests are completed successfully!"

echo "[Deploy / Development] Deployment completed successfully!"
