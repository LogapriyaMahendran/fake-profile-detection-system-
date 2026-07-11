# Production Deployment Guide

This document describes the process of deploying the **Intelligent Fake Profile Detection System** to an enterprise production environment using **Nginx**, **Gunicorn**, **Systemd**, and a dedicated **MySQL database** server on Ubuntu Linux.

---

## 🏗️ Production Tech Stack

- **Operating System**: Ubuntu 22.04 LTS
- **Application Server**: Python Flask inside Gunicorn WSGI
- **Reverse Proxy**: Nginx
- **Database**: Managed MySQL Instance (or local MySQL server)
- **Process Supervision**: Systemd
- **Security**: Let's Encrypt SSL (HTTPS)

---

## 🚀 Execution Steps

### Step 1: System Installation
Log in to your Ubuntu Server and install dependencies:
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx mysql-server git
```

### Step 2: Database Setup
1. Open MySQL command line:
   ```bash
   sudo mysql -u root
   ```
2. Create the database and user:
   ```sql
   CREATE DATABASE fake_profile_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'fakeprofile_user'@'localhost' IDENTIFIED BY 'production_secure_pass_2026';
   GRANT ALL PRIVILEGES ON fake_profile_db.* TO 'fakeprofile_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```
3. Import the database schema structure:
   ```bash
   mysql -u fakeprofile_user -p fake_profile_db < database.sql
   ```

### Step 3: Pull Codebase and Setup Environment
1. Clone the project code to your server (e.g. into `/var/www/fakeprofile`):
   ```bash
   sudo mkdir -p /var/www/fakeprofile
   sudo chown -R $USER:$USER /var/www/fakeprofile
   # copy files...
   ```
2. Navigate to directory and set up virtual environment:
   ```bash
   cd /var/www/fakeprofile
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Update [config.py](file:///c:/Users/M.Logapriya/OneDrive/Documents/Desktop/fakeprofile%20detection%201/config.py):
   - Set `USE_SQLITE = False`
   - Set `DB_USER = 'fakeprofile_user'`
   - Set `DB_PASSWORD = 'production_secure_pass_2026'`
   - Change `SECRET_KEY` to a cryptographically secure random string.
4. Pre-train the model:
   ```bash
   python train_model.py
   ```

### Step 4: Configure Systemd Service Manager
Create a systemd unit file to supervise the Flask/Gunicorn app process.
1. Open new service file:
   ```bash
   sudo nano /etc/systemd/system/fakeprofile.service
   ```
2. Paste the following configuration:
   ```ini
   [Unit]
   Description=Gunicorn instance to serve Fake Profile Detection System
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/var/www/fakeprofile
   Environment="PATH=/var/www/fakeprofile/venv/bin"
   ExecStart=/var/www/fakeprofile/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable and start service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start fakeprofile
   sudo systemctl enable fakeprofile
   ```

### Step 5: Configure Nginx as Reverse Proxy
1. Create a server site file:
   ```bash
   sudo nano /etc/nginx/sites-available/fakeprofile
   ```
2. Paste server block configuration (change `example.com` to your domain):
   ```nginx
   server {
       listen 80;
       server_name example.com www.example.com;

       location / {
           include proxy_params;
           proxy_pass http://127.0.0.1:5000;
           proxy_redirect off;
       }

       location /static/ {
           alias /var/www/fakeprofile/static/;
       }
   }
   ```
3. Enable website configuration and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/fakeprofile /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Step 6: Security Verification (HTTPS Installation)
Acquire SSL Certificates via Let's Encrypt:
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```
Follow prompts to activate auto-redirects. Traffic is now encrypted.
