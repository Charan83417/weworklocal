#!/bin/bash

# WeWorkLocal VPS Setup Script for Hostinger
# Run this script as root user on fresh Ubuntu VPS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script as root (use sudo)"
    exit 1
fi

print_header "WeWorkLocal VPS Setup - Hostinger"

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install required packages
print_status "Installing system packages..."
apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib redis-server \
    nginx git curl wget unzip \
    supervisor certbot python3-certbot-nginx \
    build-essential libpq-dev

# Create application user
print_status "Creating application user..."
if ! id "weworklocal" &>/dev/null; then
    adduser --disabled-password --gecos "" weworklocal
    usermod -aG sudo weworklocal
    print_status "User 'weworklocal' created"
else
    print_warning "User 'weworklocal' already exists"
fi

# Setup PostgreSQL
print_status "Setting up PostgreSQL database..."
sudo -u postgres psql << EOF
CREATE DATABASE weworklocal_db;
CREATE USER weworklocal_user WITH PASSWORD 'WeWork2025!@#';
ALTER ROLE weworklocal_user SET client_encoding TO 'utf8';
ALTER ROLE weworklocal_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE weworklocal_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE weworklocal_db TO weworklocal_user;
\q
EOF

# Configure Redis
print_status "Configuring Redis..."
systemctl enable redis-server
systemctl start redis-server

# Create necessary directories
print_status "Creating application directories..."
mkdir -p /home/weworklocal/logs
mkdir -p /var/log/django
chown -R weworklocal:weworklocal /home/weworklocal
chown -R weworklocal:weworklocal /var/log/django

# Setup application as weworklocal user
print_status "Setting up application..."
sudo -u weworklocal bash << 'EOF'
cd /home/weworklocal

# Create project directory
mkdir -p weworklocal
cd weworklocal

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install basic Python packages
pip install --upgrade pip
pip install Django==5.2.6 gunicorn psycopg2-binary python-decouple

echo "Virtual environment created and basic packages installed"
EOF

# Configure Nginx
print_status "Configuring Nginx..."
rm -f /etc/nginx/sites-enabled/default

# Create basic Nginx configuration
cat > /etc/nginx/sites-available/weworklocal << 'EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /home/weworklocal/weworklocal/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/weworklocal/weworklocal/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    location / {
        proxy_pass http://unix:/home/weworklocal/weworklocal/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF

ln -sf /etc/nginx/sites-available/weworklocal /etc/nginx/sites-enabled/
nginx -t
systemctl enable nginx
systemctl restart nginx

# Configure firewall
print_status "Configuring firewall..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# Enable services
print_status "Enabling services..."
systemctl enable postgresql
systemctl enable redis-server
systemctl enable nginx
systemctl enable supervisor

print_header "VPS Setup Complete!"
print_status ""
print_status "✅ System packages installed"
print_status "✅ PostgreSQL database created"
print_status "✅ Redis server configured"
print_status "✅ Nginx web server configured"
print_status "✅ Application user 'weworklocal' created"
print_status "✅ Firewall configured"
print_status ""
print_status "📋 Next Steps:"
print_status "1. Upload your WeWorkLocal code to /home/weworklocal/weworklocal/"
print_status "2. Create .env file with production settings"
print_status "3. Run the deployment script as weworklocal user"
print_status ""
print_status "🔑 Database Credentials:"
print_status "   Database: weworklocal_db"
print_status "   User: weworklocal_user"
print_status "   Password: WeWork2025!@#"
print_status ""
print_status "🔄 To deploy your application:"
print_status "   su - weworklocal"
print_status "   cd weworklocal"
print_status "   ./deploy.sh"

echo ""
echo "🎉 VPS setup completed successfully!"
