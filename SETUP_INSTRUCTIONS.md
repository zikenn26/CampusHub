# MySQL Installation and Setup Instructions

## Do You Need MySQL?

**Yes, you need to install MySQL** because:
- The project is configured to use MySQL as the database
- All models are designed for MySQL compatibility
- The `mysqlclient` package in requirements.txt requires MySQL to be installed

## Installation Options

### Option 1: MySQL Server (Recommended for Production)
1. **Download MySQL Community Server:**
   - Visit: https://dev.mysql.com/downloads/mysql/
   - Download MySQL Installer for Windows
   - Choose "MySQL Installer - Community" (MSI Installer)

2. **Install MySQL:**
   - Run the installer
   - Choose "Developer Default" or "Server only"
   - Set a root password (remember this!)
   - Complete the installation

3. **Verify Installation:**
   - Open Command Prompt or PowerShell
   - Run: `mysql --version`
   - You should see the MySQL version

### Option 2: XAMPP (Easier for Development)
1. **Download XAMPP:**
   - Visit: https://www.apachefriends.org/download.html
   - Download XAMPP for Windows
   - This includes MySQL, Apache, and PHP

2. **Install XAMPP:**
   - Run the installer
   - Install to default location (usually `C:\xampp`)
   - Start MySQL from XAMPP Control Panel

3. **Default MySQL Settings:**
   - Host: `localhost`
   - Port: `3306`
   - User: `root`
   - Password: (empty by default, or set during installation)

### Option 3: MySQL via Docker (Advanced)
If you have Docker installed:
```bash
docker run --name mysql-campus-hub -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=campus_hub -p 3306:3306 -d mysql:8.0
```

## After Installing MySQL

1. **Create the database:**
   ```sql
   CREATE DATABASE campus_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Create a `.env` file** in the project root with:
   ```
   SECRET_KEY=your-secret-key-here-change-this
   DEBUG=True
   DB_NAME=campus_hub
   DB_USER=root
   DB_PASSWORD=your-mysql-root-password
   DB_HOST=localhost
   DB_PORT=3306
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Note: On Windows, you may need to install MySQL client libraries first. If `mysqlclient` fails, try:
   ```bash
   pip install pymysql
   ```
   Then modify `settings.py` to use `pymysql` instead (see alternative below).

## Alternative: Using PyMySQL (If mysqlclient installation fails)

If `mysqlclient` gives you trouble on Windows, you can use `pymysql` instead:

1. Install PyMySQL:
   ```bash
   pip install pymysql
   ```

2. Add this to `campus_hub/__init__.py`:
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

## Quick Start After MySQL Installation

1. Activate your virtual environment (if not already active)
2. Create `.env` file with database credentials
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Run development server:
   ```bash
   python manage.py runserver
   ```

