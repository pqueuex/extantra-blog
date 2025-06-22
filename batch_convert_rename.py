#!/usr/bin/env python3
"""
Enhanced Batch File Converter and Renamer
Supports multiple file types, format conversion, and flexible date-based renaming
"""

import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path
import re
import json
from typing import Dict, List, Tuple, Optional

# Import libraries with fallbacks
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Warning: Pillow not available. Image processing will be limited.")

try:
    import mutagen
    from mutagen.id3 import ID3
    from mutagen.mp3 import MP3
    from mutagen.mp4 import MP4
    from mutagen.flac import FLAC
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    print("Warning: Mutagen not available. Audio metadata extraction will be limited.")

class BatchConverter:
    def __init__(self):
        self.supported_images = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'}
        self.supported_audio = {'.mp3', '.flac', '.m4a', '.wav', '.ogg', '.aac'}
        self.supported_video = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'}
        self.supported_docs = {'.pdf', '.doc', '.docx', '.txt', '.md'}
        
        self.conversion_map = {
            # Image conversions
            '.jpg': ['.png', '.webp', '.bmp'],
            '.png': ['.jpg', '.webp', '.bmp'],
            '.webp': ['.jpg', '.png', '.bmp'],
            '.bmp': ['.jpg', '.png', '.webp'],
            
            # Audio conversions (requires ffmpeg)
            '.mp3': ['.flac', '.wav', '.ogg'],
            '.flac': ['.mp3', '.wav', '.ogg'],
            '.wav': ['.mp3', '.flac', '.ogg'],
            
            # Video conversions (requires ffmpeg)
            '.mp4': ['.webm', '.avi'],
            '.avi': ['.mp4', '.webm'],
            '.mov': ['.mp4', '.webm'],
        }
        
        self.naming_patterns = {
            'date_sequence': '{date}_{seq:03d}',
            'date_time_sequence': '{date}_{time}_{seq:03d}',
            'year_month_sequence': '{year}-{month}_{seq:03d}',
            'category_date_sequence': '{category}_{date}_{seq:03d}',
            'custom': '{custom_pattern}'
        }

    def get_file_date(self, filepath: str, file_type: str) -> datetime:
        """Extract date from file using various methods"""
        
        # Try EXIF for images
        if file_type == 'image' and PILLOW_AVAILABLE:
            date = self._get_exif_date(filepath)
            if date:
                return date
        
        # Try audio metadata
        if file_type == 'audio' and MUTAGEN_AVAILABLE:
            date = self._get_audio_date(filepath)
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

    def _get_exif_date(self, filepath: str) -> Optional[datetime]:
        """Extract date from EXIF data"""
        try:
            with Image.open(filepath) as img:
                exif_data = img._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag in ["DateTime", "DateTimeOriginal", "DateTimeDigitized"]:
                            try:
                                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                            except:
                                continue
        except Exception as e:
            print(f"Warning: Could not read EXIF from {filepath}: {e}")
        return None

    def _get_audio_date(self, filepath: str) -> Optional[datetime]:
        """Extract date from audio metadata"""
        try:
            file = mutagen.File(filepath)
            if file is None:
                return None
            
            # Try different date fields
            date_fields = ['date', 'TDRC', 'TYER', 'recording_date']
            for field in date_fields:
                if field in file:
                    date_str = str(file[field][0])
                    # Handle various date formats
                    for fmt in ['%Y-%m-%d', '%Y', '%Y-%m-%d %H:%M:%S']:
                        try:
                            return datetime.strptime(date_str[:len(fmt.replace('%', '').replace('-', '').replace(' ', '').replace(':', ''))], fmt)
                        except:
                            continue
        except Exception as e:
            print(f"Warning: Could not read audio metadata from {filepath}: {e}")
        return None

    def _get_filename_date(self, filepath: str) -> Optional[datetime]:
        """Extract date from filename patterns"""
        filename = os.path.basename(filepath)
        
        patterns = [
            # PXL_20240125_043347823.MP.jpg
            (r'PXL_(\d{8})_(\d{6})', '%Y%m%d%H%M%S'),
            # IMG_20240125_043347.jpg
            (r'IMG_(\d{8})_(\d{6})', '%Y%m%d%H%M%S'),
            # 20240125_043347.jpg
            (r'(\d{8})_(\d{6})', '%Y%m%d%H%M%S'),
            # 2024-01-25_04-33-47.jpg
            (r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})', '%Y-%m-%d_%H-%M-%S'),
            # 20240125.jpg
            (r'(\d{8})', '%Y%m%d'),
            # 2024-01-25.jpg
            (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
        ]
        
        for pattern, fmt in patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    date_str = ''.join(match.groups())
                    return datetime.strptime(date_str, fmt.replace('-', '').replace('_', '').replace(':', ''))
                except:
                    continue
        
        return None

    def detect_file_type(self, filepath: str) -> str:
        """Detect file type based on extension"""
        ext = Path(filepath).suffix.lower()
        
        if ext in self.supported_images:
            return 'image'
        elif ext in self.supported_audio:
            return 'audio'
        elif ext in self.supported_video:
            return 'video'
        elif ext in self.supported_docs:
            return 'document'
        else:
            return 'other'

    def convert_image(self, input_path: str, output_path: str, quality: int = 95) -> bool:
        """Convert image format"""
        if not PILLOW_AVAILABLE:
            print(f"Error: Pillow not available for image conversion")
            return False
        
        try:
            with Image.open(input_path) as img:
                # Convert RGBA to RGB for JPEG
                if output_path.lower().endswith('.jpg') and img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Save with quality settings
                save_kwargs = {}
                if output_path.lower().endswith(('.jpg', '.jpeg')):
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                elif output_path.lower().endswith('.png'):
                    save_kwargs['optimize'] = True
                elif output_path.lower().endswith('.webp'):
                    save_kwargs['quality'] = quality
                    save_kwargs['method'] = 6
                
                img.save(output_path, **save_kwargs)
                return True
        except Exception as e:
            print(f"Error converting {input_path}: {e}")
            return False

    def convert_audio(self, input_path: str, output_path: str) -> bool:
        """Convert audio format using ffmpeg"""
        try:
            import subprocess
            cmd = ['ffmpeg', '-i', input_path, '-y', output_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Error converting {input_path}: {e}")
            return False

    def generate_new_filename(self, file_date: datetime, sequence: int, 
                            pattern: str, original_path: str, 
                            category: str = None) -> str:
        """Generate new filename based on pattern"""
        
        ext = Path(original_path).suffix.lower()
        date_str = file_date.strftime('%Y%m%d')
        time_str = file_date.strftime('%H%M%S')
        year = file_date.strftime('%Y')
        month = file_date.strftime('%m')
        
        format_dict = {
            'date': date_str,
            'time': time_str,
            'year': year,
            'month': month,
            'seq': sequence,
            'category': category or 'file',
            'ext': ext
        }
        
        if pattern in self.naming_patterns:
            filename_pattern = self.naming_patterns[pattern]
        else:
            filename_pattern = pattern
        
        try:
            base_name = filename_pattern.format(**format_dict)
            return f"{base_name}{ext}"
        except KeyError as e:
            print(f"Warning: Invalid pattern key {e}, using default")
            return f"{date_str}_{sequence:03d}{ext}"

    def process_directory(self, directory: str, output_dir: str = None, 
                         convert_to: str = None, naming_pattern: str = 'date_sequence',
                         file_types: List[str] = None, dry_run: bool = False,
                         quality: int = 95, backup: bool = True) -> Dict:
        """Process all files in a directory"""
        
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")
        
        if output_dir is None:
            output_dir = directory
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create backup directory if needed
        if backup and not dry_run:
            backup_dir = os.path.join(output_dir, 'original_backup')
            os.makedirs(backup_dir, exist_ok=True)
        
        # Collect files
        files_to_process = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                file_type = self.detect_file_type(filepath)
                if file_types is None or file_type in file_types:
                    files_to_process.append((filepath, file_type))
        
        print(f"Found {len(files_to_process)} files to process...")
        
        # Extract dates and sort
        files_with_dates = []
        for filepath, file_type in files_to_process:
            file_date = self.get_file_date(filepath, file_type)
            files_with_dates.append((file_date, filepath, file_type))
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
        
        current_date = None
        sequence = 1
        
        for file_date, original_path, file_type in files_with_dates:
            try:
                # Reset sequence for new dates
                date_str = file_date.strftime('%Y%m%d')
                if current_date != date_str:
                    current_date = date_str
                    sequence = 1
                
                # Generate new filename
                new_filename = self.generate_new_filename(
                    file_date, sequence, naming_pattern, original_path, file_type
                )
                
                # Handle conversion
                if convert_to:
                    new_filename = Path(new_filename).stem + convert_to
                
                new_filepath = os.path.join(output_dir, new_filename)
                
                if dry_run:
                    print(f"[DRY RUN] {os.path.basename(original_path)} -> {new_filename}")
                    if convert_to:
                        print(f"          Would convert to {convert_to}")
                    results['details'].append({
                        'original': original_path,
                        'new': new_filepath,
                        'converted': bool(convert_to)
                    })
                    results['processed'] += 1
                else:
                    # Backup original if requested
                    if backup:
                        backup_path = os.path.join(backup_dir, os.path.basename(original_path))
                        shutil.copy2(original_path, backup_path)
                    
                    # Convert or copy file
                    success = False
                    if convert_to:
                        if file_type == 'image' and convert_to in self.supported_images:
                            success = self.convert_image(original_path, new_filepath, quality)
                        elif file_type == 'audio' and convert_to in self.supported_audio:
                            success = self.convert_audio(original_path, new_filepath)
                        else:
                            print(f"Warning: Conversion from {Path(original_path).suffix} to {convert_to} not supported")
                            shutil.copy2(original_path, new_filepath)
                            success = True
                    else:
                        # Just rename/move
                        shutil.move(original_path, new_filepath)
                        success = True
                    
                    if success:
                        print(f"Processed: {os.path.basename(original_path)} -> {new_filename}")
                        results['processed'] += 1
                    else:
                        print(f"Error processing: {os.path.basename(original_path)}")
                        results['errors'] += 1
                
                sequence += 1
                
            except Exception as e:
                print(f"Error processing {original_path}: {e}")
                results['errors'] += 1
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Batch convert and rename files by date')
    parser.add_argument('directory', help='Directory to process')
    parser.add_argument('-o', '--output', help='Output directory (default: same as input)')
    parser.add_argument('-c', '--convert', help='Convert to format (e.g., .jpg, .png, .mp3)')
    parser.add_argument('-p', '--pattern', default='date_sequence', 
                       choices=['date_sequence', 'date_time_sequence', 'year_month_sequence', 'category_date_sequence'],
                       help='Naming pattern to use')
    parser.add_argument('-t', '--types', nargs='+', 
                       choices=['image', 'audio', 'video', 'document', 'other'],
                       help='File types to process (default: all)')
    parser.add_argument('-q', '--quality', type=int, default=95,
                       help='Quality for image conversion (1-100)')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip creating backup of original files')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without applying them')
    
    args = parser.parse_args()
    
    converter = BatchConverter()
    
    try:
        results = converter.process_directory(
            directory=args.directory,
            output_dir=args.output,
            convert_to=args.convert,
            naming_pattern=args.pattern,
            file_types=args.types,
            dry_run=args.dry_run,
            quality=args.quality,
            backup=not args.no_backup
        )
        
        print(f"\n{'DRY RUN ' if args.dry_run else ''}Results:")
        print(f"Processed: {results['processed']}")
        print(f"Errors: {results['errors']}")
        print(f"Skipped: {results['skipped']}")
        
        if args.dry_run:
            print(f"\nTo apply these changes, run without --dry-run")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
