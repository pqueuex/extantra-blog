import os
import json
from datetime import datetime

def generate_photos_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    photos_dir = os.path.join(base_dir, "photos")
    output_file = os.path.join(base_dir, "photos-database.json")
    
    if not os.path.exists(photos_dir):
        print(f"❌ Error: Folder not found at {photos_dir}")
        return None
    
    photo_files = [f for f in sorted(os.listdir(photos_dir)) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]
    photos_data = []
    
    for i, filename in enumerate(photo_files, 1):
        file_path = os.path.join(photos_dir, filename)
        
        # Default values from File System
        mtime = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(mtime)
        year, month, day = dt.strftime('%Y'), dt.strftime('%m'), dt.strftime('%d')
        
        # Try to override with filename date if available (YYYYMMDD)
        date_part = filename.split('_')[0]
        if len(date_part) >= 8 and date_part[:8].isdigit():
            year, month, day = date_part[:4], date_part[4:6], date_part[6:8]

        # Categorization Logic
        if int(year) <= 2009:
            category, camera = "Archive", "Sony DSC"
        elif int(year) <= 2023:
            category, camera = "Recent", "Digital Camera"
        else:
            category, camera = "Latest", "Google Pixel"

        photos_data.append({
            "id": i,
            "filename": filename,
            "title": f"Photo {year} #{i}",
            "date": f"{year}-{month}-{day}",
            "year": year,
            "category": category,
            "description": f"Captured in {year}",
            "camera": camera,
            "location": "Unknown"
        })

    database = {"photos": photos_data, "metadata": {"total_photos": len(photos_data), "generated": datetime.now().isoformat()}}
    with open(output_file, "w") as f:
        json.dump(database, f, indent=2)
    return database

if __name__ == "__main__":
    generate_photos_database()
    print("✅ Database updated with all files!")