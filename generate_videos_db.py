#!/usr/bin/env python3
"""
Generate videos database with metadata
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

def get_video_metadata(file_path):
    """Get detailed video metadata using ffprobe"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
    return None

def extract_title_from_filename(filename, video_info, date_obj, index):
    """Generate simple numbered title with metadata"""
    # Just use arbitrary numbering with metadata
    duration_str = format_duration(video_info['duration'])
    resolution = f"{video_info['width']}x{video_info['height']}"
    year = date_obj.strftime('%Y')
    
    return f"Video {index + 1:02d} - {duration_str} - {resolution} - {year}"

def get_video_info(file_path, metadata):
    """Extract video information from metadata"""
    info = {
        'duration': 0,
        'width': 0,
        'height': 0,
        'fps': 0,
        'bitrate': 0,
        'video_codec': 'unknown',
        'audio_codec': 'unknown',
        'file_size': 0
    }
    
    try:
        # File size
        info['file_size'] = os.path.getsize(file_path)
        
        if not metadata:
            return info
        
        # Format information
        format_info = metadata.get('format', {})
        info['duration'] = float(format_info.get('duration', 0))
        info['bitrate'] = int(format_info.get('bit_rate', 0))
        
        # Stream information
        video_stream = None
        audio_stream = None
        
        for stream in metadata.get('streams', []):
            if stream.get('codec_type') == 'video' and not video_stream:
                video_stream = stream
            elif stream.get('codec_type') == 'audio' and not audio_stream:
                audio_stream = stream
        
        if video_stream:
            info['width'] = int(video_stream.get('width', 0))
            info['height'] = int(video_stream.get('height', 0))
            info['video_codec'] = video_stream.get('codec_name', 'unknown')
            
            # Calculate FPS
            fps_str = video_stream.get('r_frame_rate', '0/1')
            if '/' in fps_str:
                try:
                    num, den = fps_str.split('/')
                    info['fps'] = round(float(num) / float(den), 2)
                except:
                    info['fps'] = 0
        
        if audio_stream:
            info['audio_codec'] = audio_stream.get('codec_name', 'unknown')
    
    except Exception as e:
        print(f"Error processing video info for {file_path}: {e}")
    
    return info

def format_duration(seconds):
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def format_file_size(bytes_size):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"

def main():
    videos_dir = Path('/Users/jj/extantra-blog/videos')
    
    # Find all MP4 files (after conversion)
    video_files = list(videos_dir.glob('*.mp4'))
    video_files.sort()  # Already sorted by date due to naming convention
    
    print(f"Found {len(video_files)} video files")
    
    videos_data = []
    
    for index, video_file in enumerate(video_files):
        print(f"Processing: {video_file.name}")
        
        # Get metadata
        metadata = get_video_metadata(str(video_file))
        video_info = get_video_info(str(video_file), metadata)
        
        # Extract date from filename (YYYYMMDD_XXX.mp4)
        filename_parts = video_file.stem.split('_')
        if len(filename_parts) >= 2 and filename_parts[0].isdigit() and len(filename_parts[0]) == 8:
            date_str = filename_parts[0]
            date_obj = datetime.strptime(date_str, '%Y%m%d')
        else:
            date_obj = datetime.fromtimestamp(video_file.stat().st_mtime)
        
        # Create video entry
        video_entry = {
            'filename': video_file.name,
            'title': extract_title_from_filename(video_file.name, video_info, date_obj, index),
            'date': date_obj.strftime('%Y-%m-%d'),
            'duration': video_info['duration'],
            'duration_formatted': format_duration(video_info['duration']),
            'width': video_info['width'],
            'height': video_info['height'],
            'resolution': f"{video_info['width']}x{video_info['height']}",
            'fps': video_info['fps'],
            'bitrate': video_info['bitrate'],
            'video_codec': video_info['video_codec'],
            'audio_codec': video_info['audio_codec'],
            'file_size': video_info['file_size'],
            'file_size_formatted': format_file_size(video_info['file_size']),
            'category': 'video',  # Could be expanded later
            'tags': []  # Could be expanded later
        }
        
        videos_data.append(video_entry)
    
    # Create database
    database = {
        'generated': datetime.now().isoformat(),
        'total_videos': len(videos_data),
        'total_duration': sum(v['duration'] for v in videos_data),
        'total_size': sum(v['file_size'] for v in videos_data),
        'videos': videos_data
    }
    
    # Add formatted totals
    database['total_duration_formatted'] = format_duration(database['total_duration'])
    database['total_size_formatted'] = format_file_size(database['total_size'])
    
    # Save database
    db_path = videos_dir.parent / 'videos-database.json'
    with open(db_path, 'w') as f:
        json.dump(database, f, indent=2)
    
    print(f"\n✅ Database generated successfully!")
    print(f"📄 Saved to: {db_path}")
    print(f"📹 Total videos: {database['total_videos']}")
    print(f"⏱️  Total duration: {database['total_duration_formatted']}")
    print(f"💾 Total size: {database['total_size_formatted']}")

if __name__ == '__main__':
    main()
