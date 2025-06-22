#!/bin/bash

# Alternative deployment script using cp instead of rsync
# Run this script as root on your Ubuntu/Debian server

set -e

echo "🚀 Starting production deployment for extantra.net (using cp)..."

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

# Install required packages (without rsync)
echo "🔧 Installing Nginx and Certbot..."
apt install -y nginx certbot python3-certbot-nginx ufw

# Create site directory
echo "📁 Setting up site directory..."
mkdir -p $SITE_DIR
chown -R www-data:www-data $SITE_DIR

# Copy site files using cp (excluding unwanted files)
echo "📋 Copying site files..."
find $CURRENT_DIR -maxdepth 1 -type f \( \
    -name "*.html" -o \
    -name "*.css" -o \
    -name "*.js" -o \
    -name "*.json" -o \
    -name "*.txt" -o \
    -name "*.md" \
    \) ! -name "README.md" ! -name "BATCH_PROCESSING_GUIDE.md" ! -name "DEPLOYMENT.md" \
    -exec cp {} $SITE_DIR/ \;

# Copy directories (media folders)
for dir in images audio drawings photos videos 3d models; do
    if [ -d "$CURRENT_DIR/$dir" ]; then
        echo "📁 Copying $dir directory..."
        cp -r "$CURRENT_DIR/$dir" "$SITE_DIR/"
    fi
done

# Remove any accidentally copied unwanted files
echo "🧹 Cleaning up unwanted files..."
find $SITE_DIR -name "*.py" -delete 2>/dev/null || true
find $SITE_DIR -name "*.pyc" -delete 2>/dev/null || true
find $SITE_DIR -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find $SITE_DIR -name ".DS_Store" -delete 2>/dev/null || true
find $SITE_DIR -name "batch_*" -delete 2>/dev/null || true
find $SITE_DIR -name "demo_*" -delete 2>/dev/null || true
find $SITE_DIR -name "simple_*" -delete 2>/dev/null || true
find $SITE_DIR -name "generate_*" -delete 2>/dev/null || true
find $SITE_DIR -name "deploy-*" -delete 2>/dev/null || true
find $SITE_DIR -name "nginx-*" -delete 2>/dev/null || true
find $SITE_DIR -name "setup-*" -delete 2>/dev/null || true
find $SITE_DIR -name "update-*" -delete 2>/dev/null || true
rm -f $SITE_DIR/README.md $SITE_DIR/BATCH_PROCESSING_GUIDE.md $SITE_DIR/DEPLOYMENT.md 2>/dev/null || true

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

# Enable temporary site (without removing existing sites)
echo "🔧 Enabling site configuration..."
ln -sf /etc/nginx/sites-available/${DOMAIN}-temp /etc/nginx/sites-enabled/${DOMAIN}-temp
# Only remove default if it exists and no other sites are configured
if [ -f /etc/nginx/sites-enabled/default ] && [ "$(ls -1 /etc/nginx/sites-enabled/ | wc -l)" -eq 1 ]; then
    rm -f /etc/nginx/sites-enabled/default
    echo "   Removed default site (no other sites detected)"
else
    echo "   Keeping existing site configurations"
fi

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

echo ""
echo "📋 Files copied to $SITE_DIR:"
ls -la $SITE_DIR
