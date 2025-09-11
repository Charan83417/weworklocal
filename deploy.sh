#!/bin/bash

# WeWorkLocal Deployment Script for Hostinger VPS
# Run this script as the weworklocal user

set -e  # Exit on any error

echo "🚀 Starting WeWorkLocal deployment..."

# Configuration
PROJECT_DIR="/home/weworklocal/weworklocal"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="/home/weworklocal/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if running as correct user
if [ "$USER" != "weworklocal" ]; then
    print_error "This script must be run as the 'weworklocal' user"
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p $LOG_DIR
mkdir -p $PROJECT_DIR/staticfiles
mkdir -p $PROJECT_DIR/media

# Navigate to project directory
cd $PROJECT_DIR

# Pull latest code (if using git)
if [ -d ".git" ]; then
    print_status "Pulling latest code from repository..."
    git pull origin main
else
    print_warning "Not a git repository. Skipping git pull."
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install/update dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Please create it from .env.production template"
    print_warning "Copy .env.production to .env and update the values"
fi

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate --settings=weworklocal.production_settings

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput --settings=weworklocal.production_settings

# Create superuser if it doesn't exist
print_status "Checking for superuser..."
python manage.py shell --settings=weworklocal.production_settings << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='weworkadmin').exists():
    User.objects.create_superuser('weworkadmin', 'admin@weworklocal.com', 'weworklocal@2025')
    print("Superuser 'weworkadmin' created")
else:
    print("Superuser 'weworkadmin' already exists")
EOF

# Setup admin permissions
print_status "Setting up admin permissions..."
python manage.py setup_admin_permissions --settings=weworklocal.production_settings

# Populate test data (optional)
read -p "Do you want to populate test data? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Populating test data..."
    python manage.py populate_test_data --settings=weworklocal.production_settings
fi

# Set correct permissions
print_status "Setting file permissions..."
chmod -R 755 $PROJECT_DIR
chmod -R 644 $PROJECT_DIR/staticfiles
chmod -R 644 $PROJECT_DIR/media
chmod +x $PROJECT_DIR/manage.py

# Test Django configuration
print_status "Testing Django configuration..."
python manage.py check --settings=weworklocal.production_settings

# Restart services
print_status "Restarting application services..."
sudo supervisorctl restart weworklocal_group

# Check service status
print_status "Checking service status..."
sudo supervisorctl status weworklocal_group

# Test Nginx configuration
print_status "Testing Nginx configuration..."
sudo nginx -t

# Reload Nginx
print_status "Reloading Nginx..."
sudo systemctl reload nginx

print_status "✅ Deployment completed successfully!"
print_status ""
print_status "🌐 Your application should now be accessible at:"
print_status "   - Website: http://yourdomain.com (or your VPS IP)"
print_status "   - Admin Panel: http://yourdomain.com/admin/"
print_status ""
print_status "🔑 Admin Credentials:"
print_status "   - Username: weworkadmin"
print_status "   - Password: weworklocal@2025"
print_status ""
print_status "📊 To monitor your application:"
print_status "   - Application logs: sudo tail -f /var/log/supervisor/weworklocal.log"
print_status "   - Nginx logs: sudo tail -f /var/log/nginx/error.log"
print_status "   - Service status: sudo supervisorctl status"
print_status ""
print_status "🔄 To update your application in the future:"
print_status "   - Run this script again: ./deploy.sh"

echo "🎉 WeWorkLocal deployment completed!"
