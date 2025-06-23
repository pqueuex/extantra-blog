#!/bin/bash

# Clear cache and force update script for EXTANTRA blog
echo "🚀 Clearing caches and forcing updates..."

# Clear nginx cache if it exists
if command -v nginx &> /dev/null; then
    echo "📁 Clearing nginx cache..."
    sudo find /var/cache/nginx -type f -delete 2>/dev/null || echo "No nginx cache found or no permission"
fi

# Force git pull (if this is a git repo)
if [ -d ".git" ]; then
    echo "📡 Pulling latest changes from git..."
    git pull
fi

# Update file timestamps to force cache invalidation
echo "⏰ Updating file timestamps..."
touch *.html *.css *.json *.js 2>/dev/null || true

# If using systemctl, restart nginx
if command -v systemctl &> /dev/null; then
    echo "🔄 Restarting nginx..."
    sudo systemctl reload nginx 2>/dev/null || echo "Could not reload nginx (no permission or not installed)"
fi

echo "✅ Cache clearing complete!"
echo ""
echo "💡 Additional steps you can take:"
echo "   1. Clear browser cache (Ctrl+Shift+Delete)"
echo "   2. Open site in incognito/private mode"
echo "   3. Add ?v=$(date +%s) to URLs for testing"
echo ""
echo "🔍 Current file timestamps:"
ls -la *.html *.css *.json 2>/dev/null || echo "Some files not found"
