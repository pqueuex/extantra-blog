#!/bin/bash

# Production deployment script for extantra.net
# Run this script as root on your Ubuntu/Debian server

set -e

echo "🚀 Starting production deployment for extantra.net..."

# Variables
DOMAIN="extantra.net"
SITE_DIR="/var/www/$DOMAIN"
CURRENT_DIR=$(pwd)

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install required packages
echo "🔧 Installing Nginx and Certbot..."
apt install -y nginx certbot python3-certbot-nginx ufw

# Create site directory
echo "📁 Setting up site directory..."
mkdir -p $SITE_DIR
chown -R www-data:www-data $SITE_DIR

# Copy site files (excluding unwanted files)
echo "📋 Copying site files..."
rsync -av --exclude='.git' \
          --exclude='*.py' \
          --exclude='*.pyc' \
          --exclude='__pycache__' \
          --exclude='.DS_Store' \
          --exclude='README.md' \
          --exclude='BATCH_PROCESSING_GUIDE.md' \
          --exclude='batch_*' \
          --exclude='demo_*' \
          --exclude='simple_*' \
          --exclude='generate_*' \
          --exclude='deploy-*' \
          --exclude='nginx-*' \
          $CURRENT_DIR/ $SITE_DIR/

# Set proper permissions
chown -R www-data:www-data $SITE_DIR
find $SITE_DIR -type d -exec chmod 755 {} \;
find $SITE_DIR -type f -exec chmod 644 {} \;

# Copy Nginx configuration
echo "⚙️  Setting up Nginx configuration..."
cp $CURRENT_DIR/nginx-extantra.conf /etc/nginx/sites-available/$DOMAIN

# Create temporary Nginx config for initial setup (without SSL)
cat > /etc/nginx/sites-available/${DOMAIN}-temp << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    root $SITE_DIR;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ =404;
    }
    
    location ~ /\. {
        deny all;
    }
}
EOF

# Enable temporary site
ln -sf /etc/nginx/sites-available/${DOMAIN}-temp /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
nginx -t

# Start Nginx
echo "🔄 Starting Nginx..."
systemctl enable nginx
systemctl restart nginx

# Configure firewall
echo "🔥 Configuring firewall..."
ufw allow 'Nginx Full'
ufw allow ssh
ufw --force enable

echo "⏳ Nginx is now running on port 80."
echo "📍 Please point your domain $DOMAIN to this server's IP address now."
echo ""
echo "Once your domain is pointing here, run the SSL setup:"
echo "sudo bash setup-ssl.sh"
