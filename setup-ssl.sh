#!/bin/bash

# SSL setup script for extantra.net
# Run this AFTER your domain is pointing to the server

set -e

DOMAIN="extantra.net"

echo "🔒 Setting up SSL certificate for $DOMAIN..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Test if domain is pointing to this server
echo "🧪 Testing domain resolution..."
if ! curl -s --connect-timeout 10 http://$DOMAIN | grep -q "extantra"; then
    echo "⚠️  Warning: Domain might not be pointing to this server yet."
    echo "Please ensure $DOMAIN points to this server's IP before continuing."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Obtain SSL certificate
echo "📜 Obtaining SSL certificate from Let's Encrypt..."
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# Switch to production Nginx config with SSL
echo "⚙️  Switching to production Nginx configuration..."
ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/${DOMAIN}-temp

# Test and reload Nginx
echo "🧪 Testing Nginx configuration..."
nginx -t

echo "🔄 Reloading Nginx..."
systemctl reload nginx

# Set up automatic certificate renewal
echo "🔄 Setting up automatic certificate renewal..."
systemctl enable certbot.timer
systemctl start certbot.timer

# Test SSL
echo "🔒 Testing SSL configuration..."
if curl -s --connect-timeout 10 https://$DOMAIN | grep -q "extantra"; then
    echo "✅ SSL setup complete! Your site is now live at:"
    echo "   🌐 https://$DOMAIN"
    echo "   🌐 https://www.$DOMAIN"
    echo ""
    echo "🔒 SSL Grade Test: https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
else
    echo "⚠️  SSL setup completed but site test failed. Please check manually."
fi

echo ""
echo "🎉 Deployment complete!"
echo "📋 Site features:"
echo "   ✅ HTTPS with Let's Encrypt SSL"
echo "   ✅ HTTP to HTTPS redirect"
echo "   ✅ Security headers"
echo "   ✅ Gzip compression"
echo "   ✅ Static asset caching"
echo "   ✅ Auto SSL renewal"
echo "   ✅ Private (robots.txt blocks search engines)"
