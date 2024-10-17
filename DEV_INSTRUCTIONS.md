
# Getting Started

---

---

## Installation Instructions

---

#### 1. Check if Python 3.12 is installed.
```bash
python --version
```

---

#### 2a. If Python 3.12 is not installed, download and install it.
```text
https://www.python.org/downloads/
```

#### 2b. If you are using a Linux OS, you can install Python 3.12 with the following commands as well:
```bash
sudo apt-get update
sudo apt-get install python3
```

---

#### 3. Check if pip is installed in your system.
```bash
pip --version
```

---

#### 4. If pip is not installed in your system, download and install it.
```bash
python get-pip.py
```

---

#### 5. Open your terminal and navigate to the project's root directory.

---

#### 6. Navigate to the 'src' directory of the project from the terminal.
```bash
cd src
```

---

#### 7. Check if you have Node.js and npm installed in your system.
```bash 
node -v
npm -v
```

---

#### 8. If you do not have Node.js and npm installed in your system, download and install.
```text
https://nodejs.org/en/download/package-manager/
```

---

#### 9. Install the necessary Node.js peer-dependency packages for the project.
```bash
npm install --legacy-peer-deps
```

---

#### 10. Go back to the root directory of the project.
```bash
cd ..
```

---

#### 11. Create a Python 3.12 virtual environment in the root directory of the project.
```bash
python -m venv .venv
```

---

#### 12. Activate the virtual environment.
```bash
source .venv/bin/activate
```

---

#### 13. Install the necessary Python packages for the project.
```bash
pip install -r requirements.txt
```

---

#### 14. Migrate the Django database.
```bash
python manage.py migrate
```

---

#### 15. Create an environment file called '.env' in the root directory of the project.
```bash
touch .env
```

---

#### 16. Add the following environment variables to the '.env' file.
```text
DEBUG=True
DJANGO_ENVIRONMENT="local"
SECRET_KEY="<replace_this_with_real_secret_key>"

# Update this with the actual base URL of your application
BASE_URL='http://127.0.0.1:8000'

# Service Charges
SERVICE_PROFIT_MARGIN=2.00
SERVICE_TAX_RATE=0.18

# Encryption salt (100 characters)
ENCRYPTION_SALT='<replace_this_with_real_encryption_salt>'

# Maximum assistant exports per organization
MAX_ASSISTANT_EXPORTS_ORGANIZATION=3
```

---

#### 17. Request the private environment variables from your team leader and add them to the '.env' file.
```text
SECRET_KEY
ENCRYPTION_SALT
```

---

#### 18. For DEBUG=False mode, create an environment file called '.env.prod' in the root directory of the project.
```bash
touch .env.prod
```

---

### 19. Install Redis Server

*Ubuntu*
```bash
sudo apt update
sudo apt install redis-server
```


*MacOS*

- *Brew*: If you don't already have "Homebrew" installed, you can install it by running the following command 
          in your terminal.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

```bash
brew install redis
```

*Start Redis Server*
  
  ```bash
  redis-server
  ```

---

#### 20. Run the Django server to start the application.
```bash
uvicorn config.asgi:application --host 127.0.0.1 --port 8000 --reload
```

---

#### 21. Open your web browser and navigate to the following URL.
```text
http://127.0.0.1:8000
```

---

### - *Important Instruction [1]*

#### If you need to run the application in production mode, reach the admin to provide you with the necessary environment variables, and guide you through the process if required.

---

### - *Important Instruction [2]*

#### Never add your '.env' and '.env.prod' files to the version control system as they contain sensitive information.

---

### - *Important Instruction [3]*

#### Do not add your '.idea' directory to the version control system as it contains your local development settings.

---
---

## Development Instructions

#### Starting the Celery Worker with Flower
  
  *In the first tab of the terminal window* (for processing tasks)
  ```bash
  export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
  celery -A config worker --pool solo --loglevel=info -E
  ```

  *In the second tab of the terminal window* (for scheduling tasks / cron jobs)
  ```bash
  celery -A config beat --loglevel=debug
  ```

  *In the third tab of the terminal window* (for monitoring tasks)
  ```bash
  export FLOWER_UNAUTHENTICATED_API=true
  export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
  celery -A config flower --loglevel=info -E
  ```

---

#### Forcefully Killing Celery Worker in Case of Stuck Process

*In a new terminal window*
```bash
ps auxww | grep '[c]elery worker' | awk '{print $2}' | xargs kill 
```

---


#### Public and Private SSH Keys

*For server-side operations:*

```
- Make sure you have the public and private key for the server.
```

---

#### Refreshing Documentation with Sphinx

- Locate the project's root directory in the terminal window.

*In the terminal window*
```bash
make html
```

- Copy the generated HTML files from the 'build/html' directory to the 'src/assets/docs' directory for the documentation to 
  be accessible by Django.

*In the terminal window*
```bash
cp -r build/html/* src/assets/docs/
```

---

#### Git Command to Add All Migration Files to the Tracking System & Cleaning Up Migration Files

- Go to the project's root directory in the terminal window.

*In the terminal window*
```bash
git add */migrations/*.py
git add */*/migrations/*.py
```

*For deletion*
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/*/migrations/*.py" -not -name "__init__.py" -delete
pip uninstall django --yes
pip install django
```

*For fucked-up migrations:*
```
python3 manage.py dbshell // in local
    psql -h localhost -U admin_dev -d bimod_dev // in server (dev)
    psql -h localhost -U admin_prod -d bimod_prod // in server (prod)

DELETE FROM django_migrations;
exit

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/*/migrations/*.py" -not -name "__init__.py" -delete
pip uninstall django --yes
pip install django
python3 manage.py makemigrations
python3 manage.py migrate
```

---


#### Command for Collecting the Static Files for Turning Off Debug Mode and Production Deployment

*In the terminal window*
```bash
python manage.py collectstatic
```

---


#### Using the Django Logger

'''python3
# Import the logging library
import logging

# Get the logger instance, using the module’s __name__
logger = logging.getLogger(__name__)

# Now you can log messages as needed
def my_function():
    logger.debug("Debug message from my_function")
    logger.info("Info message from my_function")
    logger.warning("Warning message from my_function")
    logger.error("Error message from my_function")
    logger.critical("Critical message from my_function")
'''
