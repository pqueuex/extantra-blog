#!/bin/bash
# Simple deployment script for testing
# Run this on your server in the project directory

echo "Starting simple HTTP server..."
echo "Your site will be available at http://your-server-ip:8080"
echo "Press Ctrl+C to stop the server"

# Python 3 method (most common)
if command -v python3 &> /dev/null; then
    python3 -m http.server 8080
# Python 2 fallback
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer 8080
# Node.js method
elif command -v npx &> /dev/null; then
    npx http-server -p 8080
else
    echo "No suitable HTTP server found. Please install Python 3 or Node.js"
    exit 1
fi
