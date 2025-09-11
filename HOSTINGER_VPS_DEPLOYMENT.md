# WeWorkLocal - Hostinger VPS Deployment Guide

## 🚀 Complete Deployment Guide for Hostinger VPS

### 📋 Prerequisites
- Hostinger VPS with Ubuntu 20.04/22.04
- Root or sudo access
- Domain name (optional but recommended)
- Basic knowledge of Linux commands

---

## 🔧 Step 1: VPS Initial Setup

### Connect to your VPS:
```bash
ssh root@your-vps-ip
```

### Update system packages:
```bash
apt update && apt upgrade -y
```

### Install required system packages:
```bash
apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git curl supervisor
```

### Create application user:
```bash
adduser weworklocal
usermod -aG sudo weworklocal
su - weworklocal
```

---

## 🗄️ Step 2: Database Setup (PostgreSQL)

### Switch to postgres user and create database:
```bash
sudo -u postgres psql
```

### In PostgreSQL shell:
```sql
CREATE DATABASE weworklocal_db;
CREATE USER weworklocal_user WITH PASSWORD 'your_secure_password';
ALTER ROLE weworklocal_user SET client_encoding TO 'utf8';
ALTER ROLE weworklocal_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE weworklocal_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE weworklocal_db TO weworklocal_user;
\q
```

---

## 📁 Step 3: Application Deployment

### Clone your repository:
```bash
cd /home/weworklocal
git clone https://github.com/yourusername/weworklocal.git
cd weworklocal
```

### Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Python dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Create environment file:
```bash
nano .env
```

### Add environment variables (see .env template below)

---

## 🔐 Step 4: Environment Configuration

### Create production settings:
```bash
nano weworklocal/production_settings.py
```

### Configure static files:
```bash
python manage.py collectstatic --noinput
```

### Run database migrations:
```bash
python manage.py migrate
```

### Create superuser:
```bash
python manage.py createsuperuser --username weworkadmin --email admin@weworklocal.com
```

### Setup admin permissions:
```bash
python manage.py setup_admin_permissions
```

### Populate test data (optional):
```bash
python manage.py populate_test_data
```

---

## 🌐 Step 5: Nginx Configuration

### Create Nginx site configuration:
```bash
sudo nano /etc/nginx/sites-available/weworklocal
```

### Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/weworklocal /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 Step 6: Gunicorn & Supervisor Setup

### Create Gunicorn configuration:
```bash
nano /home/weworklocal/weworklocal/gunicorn_config.py
```

### Create Supervisor configuration:
```bash
sudo nano /etc/supervisor/conf.d/weworklocal.conf
```

### Start services:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start weworklocal
```

---

## 🔒 Step 7: SSL Certificate (Let's Encrypt)

### Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Get SSL certificate:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🔥 Step 8: Firewall Configuration

### Configure UFW firewall:
```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 📊 Step 9: Monitoring & Maintenance

### Check application status:
```bash
sudo supervisorctl status weworklocal
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis-server
```

### View logs:
```bash
sudo tail -f /var/log/supervisor/weworklocal.log
sudo tail -f /var/log/nginx/error.log
```

---

## 🔄 Step 10: Deployment Script

### Create deployment script:
```bash
nano /home/weworklocal/deploy.sh
chmod +x /home/weworklocal/deploy.sh
```

---

## 🎯 Quick Commands

### Restart application:
```bash
sudo supervisorctl restart weworklocal
```

### Update application:
```bash
cd /home/weworklocal/weworklocal
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart weworklocal
```

### Check logs:
```bash
sudo tail -f /var/log/supervisor/weworklocal.log
```

---

## 🚨 Troubleshooting

### Common Issues:
1. **Permission denied**: Check file permissions and ownership
2. **Database connection**: Verify PostgreSQL credentials
3. **Static files not loading**: Run collectstatic and check Nginx config
4. **502 Bad Gateway**: Check Gunicorn is running and socket permissions

### Debug commands:
```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Test Gunicorn manually
cd /home/weworklocal/weworklocal
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 weworklocal.wsgi:application

# Check Nginx configuration
sudo nginx -t

# Check database connection
python manage.py dbshell
```

---

## 📱 Access Your Application

After successful deployment:
- **Website**: https://yourdomain.com
- **Admin Panel**: https://yourdomain.com/admin/
- **API**: https://yourdomain.com/api/

**Admin Credentials:**
- Username: `weworkadmin`
- Password: `weworklocal@2025`

---

## 🎉 Deployment Complete!

Your WeWorkLocal application is now running on Hostinger VPS with:
- ✅ Production-ready Django setup
- ✅ PostgreSQL database
- ✅ Redis for caching
- ✅ Nginx reverse proxy
- ✅ SSL certificate
- ✅ Process management with Supervisor
- ✅ Firewall protection
- ✅ Admin panel access
- ✅ All modules functional

**Next Steps:**
1. Configure your domain DNS to point to VPS IP
2. Test all functionality
3. Set up regular backups
4. Monitor application performance
5. Configure email settings for notifications

---

## 🎯 **Quick Deployment Commands**

### **1. Initial VPS Setup (Run as root):**
```bash
# Download and run VPS setup script
wget https://raw.githubusercontent.com/yourusername/weworklocal/main/vps_setup.sh
chmod +x vps_setup.sh
./vps_setup.sh
```

### **2. Upload Your Code:**
```bash
# Switch to application user
su - weworklocal

# Upload your code (choose one method):
# Method 1: Git clone
git clone https://github.com/yourusername/weworklocal.git

# Method 2: SCP upload from local machine
# scp -r /path/to/local/weworklocal weworklocal@your-vps-ip:/home/weworklocal/
```

### **3. Configure Environment:**
```bash
cd /home/weworklocal/weworklocal
cp .env.production .env
nano .env  # Update with your settings
```

### **4. Deploy Application:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### **5. Setup SSL Certificate:**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 📋 **Deployment Checklist**

### **Pre-Deployment:**
- [ ] VPS with Ubuntu 20.04/22.04
- [ ] Domain name configured (optional)
- [ ] SSH access to VPS
- [ ] Code repository ready

### **VPS Setup:**
- [ ] System packages updated
- [ ] PostgreSQL installed and configured
- [ ] Redis server installed
- [ ] Nginx installed
- [ ] Application user created
- [ ] Firewall configured

### **Application Deployment:**
- [ ] Code uploaded to VPS
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Superuser created
- [ ] Admin permissions setup

### **Web Server Configuration:**
- [ ] Nginx configuration created
- [ ] Gunicorn configuration created
- [ ] Supervisor configuration created
- [ ] Services started and enabled
- [ ] SSL certificate installed (optional)

### **Testing:**
- [ ] Website accessible
- [ ] Admin panel working
- [ ] User registration working
- [ ] Payment system functional
- [ ] All modules tested

### **Production Readiness:**
- [ ] Debug mode disabled
- [ ] Secret key configured
- [ ] Database backups setup
- [ ] Log monitoring configured
- [ ] Performance monitoring setup

---

## 🔧 **Configuration Files Summary**

All necessary configuration files have been created:

1. **`.env.production`** - Environment variables template
2. **`weworklocal/production_settings.py`** - Django production settings
3. **`nginx_weworklocal.conf`** - Nginx configuration
4. **`gunicorn_config.py`** - Gunicorn configuration
5. **`supervisor_weworklocal.conf`** - Supervisor configuration
6. **`deploy.sh`** - Deployment script
7. **`vps_setup.sh`** - VPS initial setup script

---

## 🚀 **One-Command Deployment**

For experienced users, here's a one-command deployment:

```bash
# Run as root on fresh VPS
curl -sSL https://raw.githubusercontent.com/yourusername/weworklocal/main/vps_setup.sh | bash
```

Then as weworklocal user:
```bash
su - weworklocal
git clone https://github.com/yourusername/weworklocal.git
cd weworklocal
cp .env.production .env
# Edit .env with your settings
nano .env
./deploy.sh
```
