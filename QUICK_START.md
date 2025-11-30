# Quick Start Guide - Campus Hub

## Step 1: Initial Setup

### 1.1 Navigate to Project Directory
```bash
cd C:\Users\rohan\OneDrive\Desktop\Gulshan_StudyMaterialPortal
```

### 1.2 Activate Virtual Environment
```bash
# On Windows PowerShell
.\venv\Scripts\Activate.ps1

# Or on Windows CMD
venv\Scripts\activate.bat
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** If `mysqlclient` fails to install on Windows, you have two options:

**Option A: Use PyMySQL (Easier)**
```bash
pip install pymysql
```
Then uncomment the lines in `campus_hub/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

**Option B: Install MySQL Client Libraries**
- Download MySQL Connector/C from: https://dev.mysql.com/downloads/connector/c/
- Or install MySQL Server which includes the client libraries

### 1.4 Set Up MySQL Database

**If MySQL is not installed:**
- Install MySQL Server or XAMPP (includes MySQL)
- Start MySQL service

#### Option A: Create New Database (First Time Setup)

**Create the database:**
```bash
# Connect to MySQL (replace with your MySQL root password)
mysql -u root -p

# Or use full path (Gulshan):
"C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe" -u root -p

# Then run in MySQL:
CREATE DATABASE campus_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### Option B: Use Existing Database (Database Already Exists)

**Check if database exists:**
```bash
# Connect to MySQL
"C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe" -u root -p

# Then run in MySQL to list all databases:
SHOW DATABASES;

# Check if 'campus_hub' exists in the list
# If it exists, you can proceed directly to Step 1.5
EXIT;
```

**If database already exists, you can:**

1. **Use the existing database as-is:**
   - Skip database creation
   - Proceed directly to Step 1.5 (Configure Environment Variables)
   - Make sure your `.env` file points to the existing database
   - Continue to Step 1.6 (Run Migrations)

2. **Reset the existing database (if you want to start fresh):**
   ```bash
   # Connect to MySQL
   "C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe" -u root -p
   
   # Then run in MySQL:
   DROP DATABASE IF EXISTS campus_hub;
   CREATE DATABASE campus_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```
   Then proceed with Step 1.6 (Run Migrations)

3. **Check existing tables in the database:**
   ```bash
   # Connect to MySQL
   "C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe" -u root -p
   
   # Then run in MySQL:
   USE campus_hub;
   SHOW TABLES;
   EXIT;
   ```
   - If tables exist, migrations have already been run
   - You can proceed to Step 1.7 (Create Superuser) or Step 1.9 (Run Server)
   - If no tables exist, proceed to Step 1.6 (Run Migrations)

### 1.5 Configure Environment Variables

Make sure your `.env` file exists in the project root with:
```
SECRET_KEY=db5imHc-Z2M0txFeoWqbXuqirP9HB2gQicCCseuhZsuMQSGpOl6E3anRQ75bCoJXaYU
DEBUG=True
DB_NAME=campus_hub
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

**Important:** Replace `your_mysql_password` with your actual MySQL root password.

### 1.6 Run Migrations

**For new database:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**For existing database:**
```bash
# Check migration status
python manage.py showmigrations

# If migrations are pending, run:
python manage.py migrate

# If you need to create new migrations (after model changes):
python manage.py makemigrations
python manage.py migrate
```

**Note:** If you see "No changes detected" when running `makemigrations`, it means all migrations are already applied.

### 1.7 Create Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin user.

### 1.8 Collect Static Files (Optional, for production)
```bash
python manage.py collectstatic --noinput
```

### 1.9 Run Development Server
```bash
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

## Step 2: Access the Application

- **Home Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Study Hub:** http://127.0.0.1:8000/materials/
- **Moderation Queue:** http://127.0.0.1:8000/materials/moderation/ (verifiers only)

## Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check `.env` file has correct database credentials
- Ensure database `campus_hub` exists

### Module Not Found Errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Migration Errors
- Delete migration files in `core/migrations/` (except `__init__.py`)
- Run `python manage.py makemigrations` again
- Run `python manage.py migrate`

### Port Already in Use
- Change port: `python manage.py runserver 8001`
- Or kill the process using port 8000


