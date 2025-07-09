#!/bin/bash

# Blog Management Script for EXTANTRA Blog
echo "🔧 EXTANTRA Blog Management"
echo "=========================="

# Function to add a new blog post
add_post() {
    echo "📝 Adding new blog post..."
    
    read -p "Post title: " title
    read -p "Post content: " content
    read -p "Tags (comma-separated): " tags
    read -p "Excerpt: " excerpt
    
    # Generate slug from title
    slug=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
    
    # Get current date
    date=$(date +%Y-%m-%d)
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
    
    echo "Generated slug: $slug"
    echo "Date: $date"
    
    read -p "Publish immediately? (y/n): " publish
    
    if [ "$publish" = "y" ]; then
        status="published"
    else
        status="draft"
    fi
    
    echo "Status: $status"
    echo "Ready to add post? (y/n)"
    read -p "Confirm: " confirm
    
    if [ "$confirm" = "y" ]; then
        echo "✅ Post would be added to database"
        echo "Note: You'll need to manually edit blog-database.json for now"
        echo ""
        echo "Post details:"
        echo "Title: $title"
        echo "Slug: $slug"
        echo "Content: $content"
        echo "Tags: $tags"
        echo "Excerpt: $excerpt"
        echo "Status: $status"
        echo "Date: $date"
    else
        echo "❌ Post creation cancelled"
    fi
}

# Function to clear all posts
clear_posts() {
    echo "🗑️  Clear all blog posts"
    echo "WARNING: This will remove all blog posts!"
    read -p "Are you sure? (type 'yes' to confirm): " confirm
    
    if [ "$confirm" = "yes" ]; then
        cat > blog-database.json << EOF
{
  "generated": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "total_posts": 0,
  "posts": []
}
EOF
        echo "✅ All blog posts cleared from database"
    else
        echo "❌ Operation cancelled"
    fi
}

# Function to list all posts
list_posts() {
    echo "📋 Current blog posts:"
    if [ -f "blog-database.json" ]; then
        echo "Database found. Posts:"
        # Simple extraction of post titles (requires jq for proper parsing)
        if command -v jq &> /dev/null; then
            jq -r '.posts[] | "- \(.title) (\(.status))"' blog-database.json
        else
            echo "(Install jq for better post listing)"
            grep -o '"title":"[^"]*"' blog-database.json | sed 's/"title":"//g' | sed 's/"//g' | while read title; do
                echo "- $title"
            done
        fi
    else
        echo "❌ No blog database found"
    fi
}

# Main menu
case "$1" in
    "add")
        add_post
        ;;
    "clear")
        clear_posts
        ;;
    "list")
        list_posts
        ;;
    *)
        echo "Usage: $0 {add|clear|list}"
        echo ""
        echo "Commands:"
        echo "  add   - Add a new blog post"
        echo "  clear - Clear all blog posts"
        echo "  list  - List all blog posts"
        echo ""
        echo "Examples:"
        echo "  $0 add"
        echo "  $0 list"
        echo "  $0 clear"
        ;;
esac
