# Prime Properties Platform

A pure Flask WSGI web application and luxury real estate platform designed for seamless local development and cPanel / CloudLinux (Passenger) production deployment.

---

## Architecture Overview

Conforms strictly to `documents/PROJECT_STRUCTURE.md`:
* **Frontend**: Static HTML pages in `frontend/`, stylesheets in `frontend/css/`, scripts in `frontend/js/`, static images in `frontend/images/`, and uploads in `frontend/uploads/`.
* **Backend**: Pure Flask WSGI in `backend/app.py`, configuration in `backend/config.py`, database models in `backend/models.py`, validation schemas in `backend/schemas.py`, pinned dependencies in `backend/requirements.txt`.
* **Documents**: Schema SQL, changelogs, architecture notes, and test reports in `documents/`.

---

## Local Development Setup

### 1. Create and Activate Virtual Environment (Target: Python 3.11)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r backend/requirements.txt
```

### 3. Database Configuration (`backend/.env`)
Copy `backend/.env.example` to `backend/.env` (or customize):
```env
FLASK_ENV=development
DEBUG=True
BEHIND_PROXY=false
PUBLIC_DOMAIN=localhost:8000
SESSION_COOKIE_SECURE=false

DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=primeproperty_v2

SECRET_KEY=primeproperty-ultra-luxury-secret-key-2026
```
*(If MySQL is not installed locally, the server automatically falls back to SQLite `primeproperty.db`).*

### 4. Seed Initial Data (Optional)
```powershell
python backend/seed_data.py
```

### 5. Run the Application
```powershell
python backend/app.py
```
Open **`http://127.0.0.1:8000`** in your browser.

---

## cPanel / CloudLinux Production Deployment

Follow the standard 10-step deployment sequence:

1. **Create MySQL Database**:
   - In cPanel → **MySQL Databases**, create database (e.g. `cpaneluser_primeproperty`) and user with full privileges.
   - Import `documents/database.sql` in phpMyAdmin.

2. **Setup Python App**:
   - In cPanel → **Setup Python App**:
     - Python Version: **3.11 (e.g. 3.11.8 / 3.11.9)**
     - Application Root: **`backend`**
     - Application Startup File: **`app.py`**
     - Application Entry Point: **`application`** (Exposed in `app.py`)

3. **Install Requirements**:
   - Click **Run Pip Install** selecting `requirements.txt` (or via CloudLinux terminal inside the virtual environment):
     ```bash
     pip install -r requirements.txt
     ```

4. **Set Production Environment Variables**:
   In cPanel Setup Python App (or `backend/.env`):
   ```env
   FLASK_ENV=production
   DEBUG=False
   BEHIND_PROXY=true
   PUBLIC_DOMAIN=app.yourdomain.com
   SESSION_COOKIE_SECURE=true

   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=cpaneluser_dbname
   MYSQL_PASSWORD=your_production_password
   MYSQL_DB=cpaneluser_dbname

   DB_POOL_SIZE=2
   DB_MAX_OVERFLOW=2
   DB_POOL_RECYCLE=280

   SECRET_KEY=generate-a-strong-random-key
   ```

5. **Restart Application**:
   - Click **Restart** in cPanel Setup Python App.

6. **Verify & Smoke Test**:
   - Load `https://app.yourdomain.com/`
   - Check SSL certificate, login session cookie (`Secure`, `HttpOnly`, `SameSite=Lax`), and properties API.
