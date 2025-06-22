#!/bin/bash

# Multi-site verification script
# Run this to check the status of all sites on your server

echo "🔍 Multi-Site Server Status Check"
echo "=================================="

# Check Nginx status
echo ""
echo "📊 Nginx Status:"
systemctl status nginx --no-pager -l | head -10

# List all enabled sites
echo ""
echo "🌐 Enabled Sites:"
ls -la /etc/nginx/sites-enabled/

# Check SSL certificates
echo ""
echo "🔒 SSL Certificates:"
if command -v certbot &> /dev/null; then
    certbot certificates
else
    echo "   Certbot not installed"
fi

# Check site directories
echo ""
echo "📁 Site Directories:"
ls -la /var/www/ 2>/dev/null || echo "   /var/www/ not found"

# Test site accessibility
echo ""
echo "🧪 Site Accessibility Tests:"

# Test extantra.net
if curl -s --connect-timeout 5 http://localhost -H "Host: extantra.net" | grep -q "extantra" 2>/dev/null; then
    echo "   ✅ extantra.net (HTTP) - responding"
else
    echo "   ❌ extantra.net (HTTP) - not responding"
fi

# Test store.extantra.net if it exists
if curl -s --connect-timeout 5 http://localhost -H "Host: store.extantra.net" >/dev/null 2>&1; then
    echo "   ✅ store.extantra.net (HTTP) - responding"
else
    echo "   ⚠️  store.extantra.net (HTTP) - not responding (may be HTTPS only)"
fi

# Check HTTPS if certificates exist
if [ -d "/etc/letsencrypt/live/extantra.net" ]; then
    if curl -s --connect-timeout 5 https://localhost -H "Host: extantra.net" --insecure | grep -q "extantra" 2>/dev/null; then
        echo "   ✅ extantra.net (HTTPS) - responding"
    else
        echo "   ❌ extantra.net (HTTPS) - not responding"
    fi
fi

if [ -d "/etc/letsencrypt/live/store.extantra.net" ]; then
    if curl -s --connect-timeout 5 https://localhost -H "Host: store.extantra.net" --insecure >/dev/null 2>&1; then
        echo "   ✅ store.extantra.net (HTTPS) - responding"
    else
        echo "   ❌ store.extantra.net (HTTPS) - not responding"
    fi
fi

# Check firewall status
echo ""
echo "🔥 Firewall Status:"
ufw status 2>/dev/null || echo "   UFW not configured"

echo ""
echo "✅ Multi-site check complete!"
