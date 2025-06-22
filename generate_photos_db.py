#!/usr/bin/env python3
"""
Generate complete photos database with metadata
"""

import os
import json
from datetime import datetime

def generate_photos_database():
    photos_dir = "/Users/jj/extantra-blog/photos"
    
    # Get all renamed photo files
    photo_files = []
    for filename in sorted(os.listdir(photos_dir)):
        if filename.endswith('.jpg') and not filename.startswith('.'):
            photo_files.append(filename)
    
    photos_data = []
    
    for i, filename in enumerate(photo_files, 1):
        # Parse date from filename (YYYYMMDD_XXX.jpg)
        date_part = filename.split('_')[0]
        year = date_part[:4]
        month = date_part[4:6]
        day = date_part[6:8]
        
        # Determine category based on year
        if int(year) <= 2009:
            category = "Archive"
            camera = "Sony DSC"
        elif int(year) <= 2023:
            category = "Recent"
            camera = "Digital Camera" if not filename.startswith(('PXL_', '20231128', '20231220', '20231225')) else "Google Pixel"
        elif int(year) == 2024:
            category = "Current"
            camera = "Google Pixel" if filename.startswith(('20240102', '20240124', '20240130', '20240215', '20240219', '20240222', '20240225', '20240331', '20240529', '20240531', '20240804')) else "Digital Camera"
        else:
            category = "Latest"
            camera = "HP Photosmart" if filename.startswith('20250116') else "Digital Camera"
        
        # Generate title
        if category == "Archive":
            title = f"Vintage {year} #{filename.split('_')[1].split('.')[0]}"
        elif category == "Recent":
            title = f"Photo {year} #{filename.split('_')[1].split('.')[0]}"
        elif category == "Current":
            title = f"Capture {year} #{filename.split('_')[1].split('.')[0]}"
        else:
            title = f"Latest {year} #{filename.split('_')[1].split('.')[0]}"
        
        # Generate description
        month_names = {
            '01': 'January', '02': 'February', '03': 'March', '04': 'April',
            '05': 'May', '06': 'June', '07': 'July', '08': 'August',
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'
        }
        
        description = f"Photography from {month_names[month]} {year}"
        
        photo_data = {
            "id": i,
            "filename": filename,
            "title": title,
            "date": f"{year}-{month}-{day}",
            "year": year,
            "category": category,
            "description": description,
            "camera": camera,
            "location": "Unknown"
        }
        
        photos_data.append(photo_data)
    
    # Create database structure
    database = {
        "photos": photos_data,
        "metadata": {
            "total_photos": len(photos_data),
            "date_range": f"{photos_data[0]['date']} to {photos_data[-1]['date']}",
            "categories": list(set(photo['category'] for photo in photos_data)),
            "generated": datetime.now().isoformat()
        }
    }
    
    return database

if __name__ == "__main__":
    database = generate_photos_database()
    
    # Write to file
    with open("/Users/jj/extantra-blog/photos-database.json", "w") as f:
        json.dump(database, f, indent=2)
    
    print(f"Generated database with {database['metadata']['total_photos']} photos")
    print(f"Date range: {database['metadata']['date_range']}")
    print(f"Categories: {', '.join(database['metadata']['categories'])}")
