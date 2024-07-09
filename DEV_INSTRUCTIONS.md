
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

#### 19. Run the Django server to start the application.
```bash
python manage.py runserver
```

---

#### 20. Open your web browser and navigate to the following URL.
```text
http://localhost:8000
```

---

### - *Important Instruction [1]*

#### 21. If you need to run the application in production mode, reach the admin to provide you with the necessary environment variables, and guide you through the process if required.

---

### - *Important Instruction [2]*

#### 22. Never add your '.env' and '.env.prod' files to the version control system as they contain sensitive information.

---

### - *Important Instruction [3]*

#### 23. Do not add your '.idea' directory to the version control system as it contains your local development settings.

---
