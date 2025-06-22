#!/bin/bash

# Site update script - run this when you want to update the live site
# This preserves the server setup and just updates the content

set -e

DOMAIN="extantra.net"
SITE_DIR="/var/www/$DOMAIN"
CURRENT_DIR=$(pwd)

echo "🔄 Updating site content..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Backup current site
echo "💾 Creating backup..."
cp -r $SITE_DIR $SITE_DIR.backup.$(date +%Y%m%d_%H%M%S)

# Update site files
echo "📋 Updating site files..."
rsync -av --delete \
          --exclude='.git' \
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
          --exclude='setup-*' \
          --exclude='update-*' \
          $CURRENT_DIR/ $SITE_DIR/

# Set proper permissions
chown -R www-data:www-data $SITE_DIR
find $SITE_DIR -type d -exec chmod 755 {} \;
find $SITE_DIR -type f -exec chmod 644 {} \;

# Test Nginx configuration
nginx -t

# Reload Nginx
systemctl reload nginx

echo "✅ Site updated successfully!"
echo "🌐 Visit: https://$DOMAIN"
