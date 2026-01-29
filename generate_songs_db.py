#!/usr/bin/env python3

import os
import json
from datetime import datetime, timezone

def generate_songs_database():
    audio_dir = "audio"
    output_file = "songs-database.json"
    
    if not os.path.exists(audio_dir):
        print(f"Error: {audio_dir} directory not found")
        return
    
    songs = []
    
    # 1. Get all audio files
    audio_files = []
    for item in os.listdir(audio_dir):
        item_path = os.path.join(audio_dir, item)
        if os.path.isfile(item_path) and item.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
            if not item.startswith('.'):
                audio_files.append(item)
    
    # 2. Sort files by creation time (getctime)
    # Use os.path.getmtime if you prefer "Last Modified" over "Created"
    audio_files.sort(key=lambda x: os.path.getctime(os.path.join(audio_dir, x)))
    
    # If you want newest songs first, uncomment the line below:
    # audio_files.reverse()

    for song_id, filename in enumerate(audio_files, start=1):
        file_path = os.path.join(audio_dir, filename)
        
        # Get the actual creation time of the file
        creation_time = os.path.getctime(file_path)
        dt_object = datetime.fromtimestamp(creation_time, tz=timezone.utc)
        
        song_entry = {
            "id": song_id,
            "filename": filename,
            "title": filename,
            "artist": "EXTANTRA",
            "album": "",
            "duration": 0,
            "duration_formatted": "0:00",
            "file_size": os.path.getsize(file_path),
            "added_date": dt_object.isoformat(), # Now uses actual file date
            "tags": [],
            "plays": 0
        }
        
        songs.append(song_entry)
    
    database = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_songs": len(songs),
        "total_duration": 0,
        "total_size": sum(song['file_size'] for song in songs),
        "songs": songs
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {output_file}")
    print(f"   📊 {len(songs)} songs processed (Sorted by Date)")
    print(f"   💾 Total size: {format_file_size(database['total_size'])}")

def format_file_size(size_bytes):
    if size_bytes == 0: return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

if __name__ == "__main__":
    generate_songs_database()