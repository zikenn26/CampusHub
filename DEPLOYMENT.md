# Campus Hub - Production Deployment Guide

This guide explains how to deploy the Campus Hub Django application to production platforms like Render or Railway.

## Prerequisites

- A GitHub repository with your code
- An account on Render or Railway
- A MySQL database (provided by the platform or external)

## Step 1: Prepare Environment Variables

### Local Development Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your local development values:
   ```env
   SECRET_KEY=your-development-secret-key
   DEBUG=True
   DB_NAME=campus_hub
   DB_USER=root
   DB_PASSWORD=your_local_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

### Generate Django Secret Key

For production, generate a secure secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 2: Static Files Collection

Before deploying, ensure static files are collected:

```bash
python manage.py collectstatic --noinput
```

This command will:
- Collect all static files from apps into `staticfiles/` directory
- Compress and optimize files using WhiteNoise
- Create manifest files for cache busting

**Note:** The `--noinput` flag prevents interactive prompts, which is required for automated deployments.

## Step 3: Database Migrations

Run migrations to set up the database schema:

```bash
python manage.py migrate
```

## Step 4: Deploy to Render

### 4.1 Create a New Web Service

1. Log in to [Render](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the repository containing Campus Hub

### 4.2 Configure Build Settings

- **Environment:** Python 3
- **Build Command:** 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- **Start Command:**
  ```
  gunicorn campus_hub.wsgi:application --bind 0.0.0.0:$PORT
  ```

### 4.3 Create Database

1. Click "New +" → "PostgreSQL" (or MySQL if available)
2. Name it `campus-hub-db`
3. Note the connection details

### 4.4 Set Environment Variables

In your web service settings, add these environment variables:

**Required:**
```
SECRET_KEY=<your-generated-secret-key>
DEBUG=False
DB_NAME=<database-name-from-render>
DB_USER=<database-user-from-render>
DB_PASSWORD=<database-password-from-render>
DB_HOST=<database-host-from-render>
DB_PORT=3306
```

**Production URLs:**
```
ALLOWED_HOSTS=your-app-name.onrender.com,your-custom-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com,https://your-custom-domain.com
```

**Important Notes:**
- Replace `your-app-name.onrender.com` with your actual Render URL
- If using a custom domain, add it to both `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- `ALLOWED_HOSTS` should be comma-separated without spaces
- `CSRF_TRUSTED_ORIGINS` should include full URLs with `https://`

### 4.5 Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Monitor the build logs for any errors

## Step 5: Deploy to Railway

### 5.1 Create a New Project

1. Log in to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository

### 5.2 Add Database

1. Click "+ New" → "Database" → "MySQL"
2. Railway will automatically create a MySQL database
3. Note the connection details from the database service

### 5.3 Configure Environment Variables

In your project settings, add environment variables:

**Required:**
```
SECRET_KEY=<your-generated-secret-key>
DEBUG=False
DB_NAME=<from-railway-database>
DB_USER=<from-railway-database>
DB_PASSWORD=<from-railway-database>
DB_HOST=<from-railway-database>
DB_PORT=3306
```

**Production URLs:**
```
ALLOWED_HOSTS=your-app-name.up.railway.app,your-custom-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app,https://your-custom-domain.com
```

### 5.4 Configure Build and Start Commands

In Railway, these are typically auto-detected, but you can set:

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```
gunicorn campus_hub.wsgi:application --bind 0.0.0.0:$PORT
```

### 5.5 Deploy

Railway will automatically detect changes and redeploy. Monitor the deployment logs.

## Step 6: Initial Setup After Deployment

### 6.1 Create Superuser

After deployment, create a superuser account:

```bash
python manage.py createsuperuser
```

Or use Railway/Render's console/SSH feature to run this command.

### 6.2 Verify Deployment

1. Visit your deployed URL
2. Check that:
   - Home page loads correctly
   - Static files (CSS) are loading
   - Database connections work
   - All features function properly

## Step 7: HTTPS and Security

### Automatic HTTPS

Both Render and Railway provide automatic HTTPS certificates. The production security settings in `settings.py` will automatically:

- Redirect HTTP to HTTPS
- Secure cookies
- Enable HSTS
- Set secure headers

### Custom Domain

If using a custom domain:

1. Add the domain in your platform's settings
2. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` environment variables
3. Wait for DNS propagation
4. The platform will automatically provision SSL certificates

## Step 8: Monitoring and Maintenance

### View Logs

- **Render:** Dashboard → Your Service → Logs
- **Railway:** Project → Deployments → View Logs

### Update Application

1. Push changes to your GitHub repository
2. Platform will automatically detect and redeploy
3. Monitor build logs for errors

### Database Backups

- **Render:** Automatic daily backups (check your plan)
- **Railway:** Configure backups in database settings

## Troubleshooting

### Static Files Not Loading

1. Verify `collectstatic` ran during build
2. Check `STATIC_ROOT` is set correctly
3. Ensure WhiteNoise middleware is in `MIDDLEWARE`
4. Check build logs for collectstatic errors

### Database Connection Errors

1. Verify all database environment variables are set
2. Check database is accessible from the platform
3. Ensure database is running and not paused
4. Verify credentials are correct

### CSRF Errors

1. Ensure `CSRF_TRUSTED_ORIGINS` includes your full domain URL with `https://`
2. Check `ALLOWED_HOSTS` includes your domain
3. Verify cookies are being set (check browser dev tools)

### 500 Internal Server Error

1. Check application logs in platform dashboard
2. Verify `DEBUG=False` in production
3. Check database migrations completed successfully
4. Ensure all environment variables are set

## Environment Variables Reference

| Variable | Description | Example |
|---------|-------------|---------|
| `SECRET_KEY` | Django secret key (required) | Generated string |
| `DEBUG` | Debug mode (False in production) | `False` |
| `DB_NAME` | Database name | `campus_hub` |
| `DB_USER` | Database username | `campus_hub_user` |
| `DB_PASSWORD` | Database password | `secure_password` |
| `DB_HOST` | Database host | `dbserver.example.com` |
| `DB_PORT` | Database port | `3306` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `yourdomain.com,www.yourdomain.com` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins | `https://yourdomain.com,https://www.yourdomain.com` |

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] `CSRF_TRUSTED_ORIGINS` includes all domains
- [ ] Database credentials are secure
- [ ] HTTPS is enabled (automatic on Render/Railway)
- [ ] Environment variables are set in platform (not in code)
- [ ] `.env` file is in `.gitignore` (never commit secrets)

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app/)

