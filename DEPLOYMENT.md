# Deployment Guide for extantra.net

## 🚀 Production Deployment

Your site is ready for production deployment with HTTPS, security headers, and optimal performance.

### Prerequisites
- Ubuntu/Debian server with root access
- Domain name (extantra.net) ready to point to your server
- Server with public IP address
- **Note**: This setup is designed to coexist with other sites (like store.extantra.net) on the same server

### Step 1: Initial Server Setup

1. **Upload your site** to your server (you mentioned it's already cloned)
2. **Run the production deployment script** as root:
   ```bash
   sudo bash deploy-production.sh
   ```

This script will:
- Install and configure Nginx
- Set up firewall rules
- Create the site directory structure
- Copy your site files (excluding development files)
- Start Nginx on port 80

### Step 2: Point Your Domain

After the script completes, point your domain `extantra.net` and `www.extantra.net` to your server's IP address using:
- A record: `extantra.net` → `your.server.ip.address`
- A record: `www.extantra.net` → `your.server.ip.address`

### Step 3: Enable HTTPS

Once your domain is pointing to the server (wait 5-10 minutes for DNS propagation), run:
```bash
sudo bash setup-ssl.sh
```

This script will:
- Obtain free SSL certificates from Let's Encrypt
- Configure HTTPS with security headers
- Set up automatic certificate renewal
- Enable HTTP to HTTPS redirects

## 🔄 Updating Your Site

When you make changes to your site locally, use the update script:
```bash
sudo bash update-site.sh
```

This will:
- Create a backup of the current site
- Upload your changes
- Reload the web server

## 🛡️ Security Features

Your deployed site includes:
- **HTTPS only** - HTTP requests redirect to HTTPS
- **Security headers** - HSTS, X-Frame-Options, etc.
- **Private site** - robots.txt blocks search engines
- **File protection** - Sensitive files (.git, .py) are blocked
- **Firewall** - UFW configured with minimal open ports

## 📊 Performance Features

- **Gzip compression** - Reduces bandwidth usage
- **Static asset caching** - Images, CSS, JS cached for 1 year
- **HTTP/2** - Modern protocol for better performance

## 🔧 Monitoring & Maintenance

### Check Site Status
```bash
sudo systemctl status nginx
sudo certbot certificates
```

### View Logs
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Manual SSL Renewal Test
```bash
sudo certbot renew --dry-run
```

## 🌐 Final URLs

After deployment, your site will be available at:
- https://extantra.net
- https://www.extantra.net

## 🆘 Troubleshooting

### Domain Not Resolving
```bash
# Check if domain points to your server
dig extantra.net
nslookup extantra.net
```

### SSL Issues
```bash
# Check certificate status
sudo certbot certificates
# Force renewal
sudo certbot renew --force-renewal
```

### Nginx Issues
```bash
# Test configuration
sudo nginx -t
# Restart service
sudo systemctl restart nginx
```

## 📁 File Structure on Server

```
/var/www/extantra.net/          # Your site files
/etc/nginx/sites-available/     # Nginx config
/etc/letsencrypt/               # SSL certificates
```

## 🏢 Multi-Site Considerations

Since you have `store.extantra.net` running on the same server:

### Site Isolation
- Each subdomain has its own Nginx configuration file
- SSL certificates are managed separately per domain
- Site files are stored in separate directories:
  - Main site: `/var/www/extantra.net/`
  - Store: `/var/www/store.extantra.net/` (existing)

### Shared Resources
- **Nginx**: Shared web server handling all subdomains
- **Certbot**: Manages SSL certificates for all domains
- **Firewall**: UFW rules apply to all sites

### DNS Configuration
Make sure your DNS has both:
- A record: `extantra.net` → `your.server.ip.address`
- A record: `store.extantra.net` → `your.server.ip.address` (existing)
- A record: `www.extantra.net` → `your.server.ip.address`

### SSL Certificate Management
The setup script will obtain certificates for `extantra.net` and `www.extantra.net` without affecting your existing `store.extantra.net` certificates.

## 🎉 Post-Deployment

1. **Test your site** at https://extantra.net
2. **Check SSL grade** at https://www.ssllabs.com/ssltest/
3. **Test mobile responsiveness**
4. **Verify admin interface** (triple-click logo)
5. **Test all gallery pages**

Your site is now live, secure, and optimized for performance!
