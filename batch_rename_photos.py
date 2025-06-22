#!/usr/bin/env python3
"""
Batch rename photos based on EXIF date metadata
Renames photos to format: YYYYMMDD_001.jpg, YYYYMMDD_002.jpg, etc.
"""

import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import re

def get_photo_date(filepath):
    """Extract date from EXIF data or filename"""
    try:
        # Try to get EXIF date first
        with Image.open(filepath) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "DateTime" or tag == "DateTimeOriginal":
                        try:
                            return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                        except:
                            continue
    except:
        pass
    
    # Fallback to filename patterns
    filename = os.path.basename(filepath)
    
    # PXL format: PXL_20240125_043347823.MP.jpg
    pxl_match = re.search(r'PXL_(\d{8})_(\d{6})', filename)
    if pxl_match:
        date_str = pxl_match.group(1)
        time_str = pxl_match.group(2)
        try:
            return datetime.strptime(f"{date_str}{time_str}", "%Y%m%d%H%M%S")
        except:
            pass
    
    # DSC format: DSC00887.JPG (assume recent if no other data)
    if filename.startswith('DSC'):
        return datetime(2024, 1, 1)  # Default date for DSC files
    
    # HPIM format: HPIM1200.JPG (assume older)
    if filename.startswith('HPIM'):
        return datetime(2023, 1, 1)  # Default date for HPIM files
    
    # IMG format: IMG_0001.jpg (assume mid-range)
    if filename.startswith('IMG_'):
        return datetime(2023, 6, 1)  # Default date for IMG files
    
    # Numeric only: 303.jpg
    if filename[0].isdigit():
        return datetime(2022, 1, 1)  # Default date for numeric files
    
    # Default fallback
    return datetime(2023, 1, 1)

def batch_rename_photos(photos_dir):
    """Batch rename all photos in chronological order"""
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG'}
    photo_files = []
    
    for filename in os.listdir(photos_dir):
        if any(filename.endswith(ext) for ext in image_extensions):
            filepath = os.path.join(photos_dir, filename)
            if os.path.isfile(filepath):
                photo_files.append(filepath)
    
    print(f"Found {len(photo_files)} photos to process...")
    
    # Extract dates and sort
    photos_with_dates = []
    for filepath in photo_files:
        photo_date = get_photo_date(filepath)
        photos_with_dates.append((photo_date, filepath))
        print(f"{os.path.basename(filepath)} -> {photo_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Sort by date
    photos_with_dates.sort(key=lambda x: x[0])
    
    # Create backup directory
    backup_dir = os.path.join(photos_dir, 'original_backup')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Rename files
    current_date = None
    counter = 1
    
    for i, (photo_date, old_filepath) in enumerate(photos_with_dates):
        # Reset counter for new dates
        date_str = photo_date.strftime('%Y%m%d')
        if current_date != date_str:
            current_date = date_str
            counter = 1
        
        # Generate new filename
        ext = os.path.splitext(old_filepath)[1].lower()
        if ext == '.jpeg':
            ext = '.jpg'
        
        new_filename = f"{date_str}_{counter:03d}{ext}"
        new_filepath = os.path.join(photos_dir, new_filename)
        
        # Backup original
        backup_filepath = os.path.join(backup_dir, os.path.basename(old_filepath))
        shutil.copy2(old_filepath, backup_filepath)
        
        # Rename file
        shutil.move(old_filepath, new_filepath)
        
        print(f"Renamed: {os.path.basename(old_filepath)} -> {new_filename}")
        counter += 1
    
    print(f"\nCompleted! Renamed {len(photos_with_dates)} photos.")
    print(f"Original files backed up to: {backup_dir}")

if __name__ == "__main__":
    photos_directory = "/Users/jj/extantra-blog/photos"
    
    # Check if directory exists
    if not os.path.exists(photos_directory):
        print(f"Error: Directory {photos_directory} does not exist")
        exit(1)
    
    # Confirm before proceeding
    print(f"This will rename all photos in {photos_directory}")
    print("Original files will be backed up to photos/original_backup/")
    response = input("Continue? (y/N): ")
    
    if response.lower() == 'y':
        batch_rename_photos(photos_directory)
    else:
        print("Operation cancelled.")
