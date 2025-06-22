#!/usr/bin/env python3
"""
Generate drawings database with metadata
"""

import os
import json
from datetime import datetime
from pathlib import Path

def generate_drawings_database():
    """Generate a database of drawings with metadata"""
    
    drawings_dir = "/Users/jj/extantra-blog/drawings"
    output_file = "/Users/jj/extantra-blog/drawings-database.json"
    
    # Get all WebP files
    drawings = []
    webp_files = [f for f in os.listdir(drawings_dir) if f.endswith('.webp')]
    webp_files.sort()  # Already sorted by date due to naming
    
    print(f"Found {len(webp_files)} drawings to process...")
    
    for i, filename in enumerate(webp_files, 1):
        filepath = os.path.join(drawings_dir, filename)
        
        # Extract date from filename
        date_str = filename.split('_')[0]  # e.g., "20240625" from "20240625_001.webp"
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            date_formatted = date_obj.strftime('%Y-%m-%d')
            year = date_obj.strftime('%Y')
        except:
            date_formatted = "2024-01-01"
            year = "2024"
        
        # Determine category based on date
        if year in ['2021', '2022']:
            category = "Archive"
        elif year == '2023':
            category = "Vintage"
        elif year == '2024':
            category = "Recent"
        else:
            category = "Latest"
        
        # Create title
        sequence = filename.split('_')[1].split('.')[0]  # e.g., "001" from "20240625_001.webp"
        title = f"Drawing {date_formatted} #{sequence}"
        
        # Get file size
        try:
            file_size = os.path.getsize(filepath)
            size_mb = round(file_size / (1024 * 1024), 2)
            file_size_str = f"{size_mb}MB"
        except:
            file_size_str = "Unknown"
        
        drawing_data = {
            "id": i,
            "filename": filename,
            "title": title,
            "date": date_formatted,
            "year": year,
            "category": category,
            "description": f"Digital artwork from {date_formatted}",
            "medium": "Digital",
            "format": "WebP",
            "size": file_size_str,
            "tags": ["digital art", "illustration", "drawing"]
        }
        
        drawings.append(drawing_data)
        print(f"Processed: {filename} -> {title}")
    
    # Create database structure
    database = {
        "metadata": {
            "total_drawings": len(drawings),
            "generated_date": datetime.now().isoformat(),
            "format": "WebP",
            "date_range": f"{drawings[0]['date']} to {drawings[-1]['date']}" if drawings else "No drawings"
        },
        "drawings": drawings
    }
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Database generated successfully!")
    print(f"📁 File: {output_file}")
    print(f"📊 Total drawings: {len(drawings)}")
    print(f"📅 Date range: {database['metadata']['date_range']}")
    
    return database

if __name__ == "__main__":
    generate_drawings_database()
