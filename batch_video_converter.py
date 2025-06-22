#!/usr/bin/env python3
"""
Batch Video Converter and Renamer
Converts videos to optimal MP4 format and renames by date
"""

import os
import shutil
import subprocess
import json
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Tuple, Optional

class BatchVideoConverter:
    def __init__(self):
        self.supported_formats = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v'}
        
        # FFmpeg settings for optimal compression
        self.ffmpeg_settings = {
            'codec': 'libx264',
            'preset': 'medium',
            'crf': '28',  # Lower = better quality, higher = smaller size (18-28 recommended)
            'audio_codec': 'aac',
            'audio_bitrate': '128k'
        }

    def get_video_date(self, filepath: str) -> datetime:
        """Extract date from video metadata or filename"""
        
        # Try to get creation date from video metadata
        date = self._get_metadata_date(filepath)
        if date:
            return date
        
        # Try filename patterns
        date = self._get_filename_date(filepath)
        if date:
            return date
        
        # Fallback to file modification time
        try:
            timestamp = os.path.getmtime(filepath)
            return datetime.fromtimestamp(timestamp)
        except:
            pass
        
        # Last resort - current time
        return datetime.now()

    def _get_metadata_date(self, filepath: str) -> Optional[datetime]:
        """Extract creation date from video metadata using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', filepath
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                import json
                metadata = json.loads(result.stdout)
                format_info = metadata.get('format', {})
                tags = format_info.get('tags', {})
                
                # Try different date fields
                date_fields = ['creation_time', 'date', 'DATE', 'com.apple.quicktime.creationdate']
                for field in date_fields:
                    if field in tags:
                        date_str = tags[field]
                        # Parse various date formats
                        for fmt in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                            try:
                                return datetime.strptime(date_str[:len(fmt.replace('%f', '000000'))], fmt)
                            except:
                                continue
        except Exception as e:
            print(f"Warning: Could not read metadata from {filepath}: {e}")
        
        return None

    def _get_filename_date(self, filepath: str) -> Optional[datetime]:
        """Extract date from common filename patterns"""
        filename = os.path.basename(filepath)
        
        patterns = [
            # Already renamed format: 20240125_001.mp4
            (r'(\d{8})_(\d{3})', lambda m: datetime.strptime(m.group(1), '%Y%m%d')),
            
            # VID00004.AVI - assume older
            (r'^VID\d+', lambda m: datetime(2020, 1, 1)),
            
            # MOV01275.AVI - assume mid-range
            (r'^MOV\d+', lambda m: datetime(2021, 1, 1)),
            
            # Numeric range: 0001-0140.mp4
            (r'^(\d{4})-(\d{4})', lambda m: datetime(2023, 1, 1)),
            
            # Movie titles - assume recent
            (r'^[a-zA-Z]', lambda m: datetime(2024, 1, 1)),
        ]
        
        for pattern, date_func in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                try:
                    return date_func(match)
                except:
                    continue
        
        return None

    def get_video_info(self, filepath: str) -> Dict:
        """Get video information using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', filepath
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                format_info = data.get('format', {})
                video_stream = None
                audio_stream = None
                
                # Find video and audio streams
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'video' and not video_stream:
                        video_stream = stream
                    elif stream.get('codec_type') == 'audio' and not audio_stream:
                        audio_stream = stream
                
                info = {
                    'duration': float(format_info.get('duration', 0)),
                    'size': int(format_info.get('size', 0)),
                    'bitrate': int(format_info.get('bit_rate', 0)),
                    'format': format_info.get('format_name', 'unknown')
                }
                
                if video_stream:
                    info.update({
                        'width': int(video_stream.get('width', 0)),
                        'height': int(video_stream.get('height', 0)),
                        'video_codec': video_stream.get('codec_name', 'unknown'),
                        'fps': eval(video_stream.get('r_frame_rate', '0/1')) if '/' in str(video_stream.get('r_frame_rate', '')) else 0
                    })
                
                if audio_stream:
                    info.update({
                        'audio_codec': audio_stream.get('codec_name', 'unknown'),
                        'audio_bitrate': int(audio_stream.get('bit_rate', 0))
                    })
                
                return info
        except Exception as e:
            print(f"Warning: Could not get video info for {filepath}: {e}")
        
        return {'duration': 0, 'size': 0, 'width': 0, 'height': 0}

    def convert_video(self, input_path: str, output_path: str) -> bool:
        """Convert video to optimized MP4 format"""
        try:
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:v', self.ffmpeg_settings['codec'],
                '-preset', self.ffmpeg_settings['preset'],
                '-crf', self.ffmpeg_settings['crf'],
                '-c:a', self.ffmpeg_settings['audio_codec'],
                '-b:a', self.ffmpeg_settings['audio_bitrate'],
                '-movflags', '+faststart',  # Optimize for web playback
                '-y',  # Overwrite output file
                output_path
            ]
            
            print(f"Converting: {os.path.basename(input_path)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                print(f"Error converting {input_path}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error converting {input_path}: {e}")
            return False

    def generate_new_filename(self, file_date: datetime, sequence: int, original_path: str) -> str:
        """Generate new filename based on date and sequence"""
        date_str = file_date.strftime('%Y%m%d')
        return f"{date_str}_{sequence:03d}.mp4"

    def process_directory(self, directory: str, output_dir: str = None, 
                         dry_run: bool = False, backup: bool = True) -> Dict:
        """Process all videos in a directory"""
        
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")
        
        if output_dir is None:
            output_dir = directory
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create backup directory if needed
        backup_dir = None
        if backup and not dry_run:
            backup_dir = os.path.join(output_dir, 'original_backup')
            os.makedirs(backup_dir, exist_ok=True)
        
        # Collect video files
        files_to_process = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                ext = Path(filepath).suffix.lower()
                if ext in self.supported_formats:
                    files_to_process.append(filepath)
        
        print(f"Found {len(files_to_process)} video files to process...")
        
        # Extract dates and sort
        files_with_dates = []
        for filepath in files_to_process:
            file_date = self.get_video_date(filepath)
            files_with_dates.append((file_date, filepath))
            print(f"{os.path.basename(filepath)} -> {file_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Sort by date
        files_with_dates.sort(key=lambda x: x[0])
        
        # Process files
        results = {
            'processed': 0,
            'errors': 0,
            'skipped': 0,
            'details': []
        }
        
        # Track sequences per date
        date_sequences = {}
        
        for file_date, original_path in files_with_dates:
            try:
                # Get sequence number for this date
                date_str = file_date.strftime('%Y%m%d')
                if date_str not in date_sequences:
                    date_sequences[date_str] = 1
                else:
                    date_sequences[date_str] += 1
                
                sequence = date_sequences[date_str]
                
                # Generate new filename
                new_filename = self.generate_new_filename(file_date, sequence, original_path)
                new_filepath = os.path.join(output_dir, new_filename)
                
                # Check if target already exists
                if os.path.exists(new_filepath) and new_filepath != original_path:
                    if dry_run:
                        print(f"[DRY RUN] WARNING: Target exists: {new_filename}")
                    else:
                        print(f"Warning: Target exists, skipping: {new_filename}")
                        results['skipped'] += 1
                        continue
                
                if dry_run:
                    print(f"[DRY RUN] {os.path.basename(original_path)} -> {new_filename}")
                    video_info = self.get_video_info(original_path)
                    print(f"          Video: {video_info.get('width')}x{video_info.get('height')}, {video_info.get('duration'):.1f}s")
                    results['details'].append({
                        'original': original_path,
                        'new': new_filepath,
                        'date': file_date.isoformat(),
                        'info': video_info
                    })
                    results['processed'] += 1
                else:
                    # Backup original if requested
                    if backup_dir and original_path != new_filepath:
                        backup_path = os.path.join(backup_dir, os.path.basename(original_path))
                        # Handle duplicate backup names
                        counter = 1
                        while os.path.exists(backup_path):
                            name, ext = os.path.splitext(os.path.basename(original_path))
                            backup_path = os.path.join(backup_dir, f"{name}_{counter}{ext}")
                            counter += 1
                        shutil.copy2(original_path, backup_path)
                    
                    # Convert and rename
                    if original_path != new_filepath:
                        success = self.convert_video(original_path, new_filepath)
                        if success:
                            # Remove original after successful conversion
                            os.remove(original_path)
                            print(f"Converted: {os.path.basename(original_path)} -> {new_filename}")
                            results['processed'] += 1
                        else:
                            print(f"Error converting: {os.path.basename(original_path)}")
                            results['errors'] += 1
                    else:
                        print(f"No conversion needed: {new_filename}")
                        results['processed'] += 1
                
            except Exception as e:
                print(f"Error processing {original_path}: {e}")
                results['errors'] += 1
        
        return results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch video converter and renamer')
    parser.add_argument('directory', help='Directory containing videos to process')
    parser.add_argument('-o', '--output', help='Output directory (default: same as input)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying them')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backup of original files')
    parser.add_argument('--crf', type=int, default=28, help='CRF value for video quality (18-28, lower = better quality)')
    
    args = parser.parse_args()
    
    # Check for FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: FFmpeg and FFprobe are required but not found in PATH")
        print("Please install FFmpeg: https://ffmpeg.org/download.html")
        return 1
    
    converter = BatchVideoConverter()
    
    # Update CRF setting if provided
    if args.crf:
        converter.ffmpeg_settings['crf'] = str(args.crf)
    
    try:
        results = converter.process_directory(
            directory=args.directory,
            output_dir=args.output,
            dry_run=args.dry_run,
            backup=not args.no_backup
        )
        
        print(f"\n{'=' * 50}")
        print(f"{'DRY RUN ' if args.dry_run else ''}RESULTS:")
        print(f"{'=' * 50}")
        print(f"Processed: {results['processed']}")
        print(f"Errors: {results['errors']}")
        print(f"Skipped: {results['skipped']}")
        
        if args.dry_run:
            print(f"\nTo apply these changes, run without --dry-run")
            print(f"Note: Requires FFmpeg for video conversion")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
