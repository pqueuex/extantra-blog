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
    song_id = 1
    
    # Get all audio files (excluding subdirectories like preferablysilentgoblin)
    audio_files = []
    for item in os.listdir(audio_dir):
        item_path = os.path.join(audio_dir, item)
        if os.path.isfile(item_path) and item.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
            audio_files.append(item)
    
    # Sort files alphabetically
    audio_files.sort()
    
    for filename in audio_files:
        if filename.startswith('.'):  # Skip hidden files
            continue
            
        file_path = os.path.join(audio_dir, filename)
        
        # Use filename as title (including extension as requested)
        display_title = filename
        
        # Create song entry
        song_entry = {
            "id": song_id,
            "filename": filename,
            "title": display_title,
            "artist": "EXTANTRA",
            "album": "",
            "duration": 0,  # We'll set this to 0 since we can't get metadata easily
            "duration_formatted": "0:00",
            "file_size": os.path.getsize(file_path),
            "added_date": datetime.now(timezone.utc).isoformat(),
            "tags": [],
            "plays": 0
        }
        
        songs.append(song_entry)
        song_id += 1
    
    # Create database structure
    database = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_songs": len(songs),
        "total_duration": 0,
        "total_size": sum(song['file_size'] for song in songs),
        "songs": songs
    }
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {output_file}")
    print(f"   📊 {len(songs)} songs processed")
    print(f"   💾 Total size: {format_file_size(database['total_size'])}")

def format_file_size(size_bytes):
    """Format file size in bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

if __name__ == "__main__":
    generate_songs_database()
