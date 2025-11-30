# **Campus Hub**
A unified academic platform for departments, faculty, study materials, moderation, timetables, and notifications.

## **Overview**
Campus Hub is a Django-based academic resource and communication system for universities and institutes. It includes:
- Department directory
- Faculty directory
- Study material uploads
- Moderation workflow
- Timetable management
- Custom user roles
- Audit logs

## **Tech Stack**
| Layer | Technology |
|-------|------------|
| **Backend** | Django 5, Python 3.11+ |
| **Database** | MySQL Server 9.5 |
| **Auth** | Custom User Model (email login) |
| **Frontend** | Django Templates, HTML, CSS |
| **File Storage** | Google Drive API (planned) |
| **Background Jobs** | Celery or RQ (planned) |

## **Project Architecture (ASCII)**
```
                  [ Frontend ]
           Django Templates + CSS
                      |
                      v
            [ Django Backend Layer ]
        Views, Forms, Auth, Permissions
                      |
            -------------------------
            |                       |
            v                       v
     [ MySQL Database ]     [ Google Drive ]
   Users, Dept, Materials      (Future)
   Timetable, Audit Logs
```

## **Folder Structure**
```
campus_hub/
├── campus_hub/
├── core/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/core/
├── venv/
├── .env
├── manage.py
└── README.md
```

# **Setup From Scratch**
## 1. Go to project directory
```
cd C:\Users\rohan\OneDrive\Desktop\Gulshan_StudyMaterialPortal
```

## 2. Activate virtual environment
PowerShell:
```
.\venv\Scripts\Activate.ps1
```

## 3. Install dependencies
```
pip install -r requirements.txt
```

## 4. Confirm MySQL is running
```
& "C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe" -u root -p
```

Check DB:
```
SHOW DATABASES;
```

## 5. Create or edit `.env`
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=campus_hub
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

## 6. Run migrations
```
python manage.py migrate
```

## 7. Create superuser
```
python manage.py createsuperuser
```

## 8. Start server
```
python manage.py runserver
```

# **Continue After Restart**
1. Enter project folder  
2. Reactivate venv  
3. Ensure MySQL is running  
4. Run server  

# **Implemented Features**
- Custom user model
- Departments module
- Faculty directory
- Study material upload + moderation
- Timetable module
- Audit logging

# **Planned Additions**
- Google Drive integration
- Notification system
- Coordinator dashboard
- PWA support

# **License**
MIT License
