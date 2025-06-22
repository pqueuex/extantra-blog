#!/usr/bin/env python3
"""
Simple Batch File Renamer
Standard library only - renames files by date with chronological numbering
"""

import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path
import re
import json
from typing import Dict, List, Tuple, Optional

class SimpleBatchRenamer:
    def __init__(self):
        self.supported_extensions = {
            '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif',  # Images
            '.mp3', '.flac', '.m4a', '.wav', '.ogg', '.aac',           # Audio
            '.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv',           # Video
            '.pdf', '.doc', '.docx', '.txt', '.md'                     # Documents
        }
        
        self.naming_patterns = {
            'date_sequence': '{date}_{seq:03d}',
            'date_time_sequence': '{date}_{time}_{seq:03d}',
            'year_month_sequence': '{year}-{month}_{seq:03d}',
            'category_date_sequence': '{category}_{date}_{seq:03d}',
        }

    def get_file_date(self, filepath: str) -> datetime:
        """Extract date from filename patterns or file stats"""
        
        # Try filename patterns first
        date = self._get_filename_date(filepath)
        if date:
            return date
        
        # Fallback to file modification time
        try:
            timestamp = os.path.getmtime(filepath)
            return datetime.fromtimestamp(timestamp)
        except:
            pass
        
        # Fallback to file creation time
        try:
            timestamp = os.path.getctime(filepath)
            return datetime.fromtimestamp(timestamp)
        except:
            pass
        
        # Last resort - current time
        return datetime.now()

    def _get_filename_date(self, filepath: str) -> Optional[datetime]:
        """Extract date from common filename patterns"""
        filename = os.path.basename(filepath)
        
        patterns = [
            # Already renamed format: 20240125_001.jpg
            (r'(\d{8})_(\d{3})', lambda m: datetime.strptime(m.group(1), '%Y%m%d')),
            
            # PXL_20240125_043347823.MP.jpg
            (r'PXL_(\d{8})_(\d{6})', lambda m: datetime.strptime(f"{m.group(1)}{m.group(2)}", '%Y%m%d%H%M%S')),
            
            # IMG_20240125_043347.jpg
            (r'IMG_(\d{8})_(\d{6})', lambda m: datetime.strptime(f"{m.group(1)}{m.group(2)}", '%Y%m%d%H%M%S')),
            
            # Screenshot 2024-01-25 at 04.33.47.png
            (r'Screenshot (\d{4})-(\d{2})-(\d{2}) at (\d{2})\.(\d{2})\.(\d{2})', 
             lambda m: datetime.strptime(f"{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}{m.group(5)}{m.group(6)}", '%Y%m%d%H%M%S')),
            
            # 20240125_043347.jpg
            (r'(\d{8})_(\d{6})', lambda m: datetime.strptime(f"{m.group(1)}{m.group(2)}", '%Y%m%d%H%M%S')),
            
            # 2024-01-25_04-33-47.jpg
            (r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})', 
             lambda m: datetime.strptime(f"{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}{m.group(5)}{m.group(6)}", '%Y%m%d%H%M%S')),
            
            # 20240125.jpg
            (r'(\d{8})', lambda m: datetime.strptime(m.group(1), '%Y%m%d')),
            
            # 2024-01-25.jpg
            (r'(\d{4})-(\d{2})-(\d{2})', lambda m: datetime.strptime(f"{m.group(1)}{m.group(2)}{m.group(3)}", '%Y%m%d')),
            
            # DSC00887.JPG (assume recent)
            (r'^DSC\d+', lambda m: datetime(2024, 1, 1)),
            
            # HPIM1200.JPG (assume older)
            (r'^HPIM\d+', lambda m: datetime(2020, 1, 1)),
            
            # IMG_0001.jpg
            (r'^IMG_\d+', lambda m: datetime(2023, 6, 1)),
            
            # Pure numeric: 303.jpg
            (r'^\d+$', lambda m: datetime(2022, 1, 1)),
        ]
        
        for pattern, date_func in patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    return date_func(match)
                except:
                    continue
        
        return None

    def detect_file_category(self, filepath: str) -> str:
        """Detect file category based on extension"""
        ext = Path(filepath).suffix.lower()
        
        image_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'}
        audio_exts = {'.mp3', '.flac', '.m4a', '.wav', '.ogg', '.aac'}
        video_exts = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'}
        doc_exts = {'.pdf', '.doc', '.docx', '.txt', '.md'}
        
        if ext in image_exts:
            return 'photo'
        elif ext in audio_exts:
            return 'audio'
        elif ext in video_exts:
            return 'video'
        elif ext in doc_exts:
            return 'document'
        else:
            return 'file'

    def generate_new_filename(self, file_date: datetime, sequence: int, 
                            pattern: str, original_path: str, 
                            category: str = None) -> str:
        """Generate new filename based on pattern"""
        
        ext = Path(original_path).suffix.lower()
        # Normalize jpeg to jpg
        if ext == '.jpeg':
            ext = '.jpg'
        
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
                         naming_pattern: str = 'date_sequence',
                         file_extensions: List[str] = None, 
                         dry_run: bool = False,
                         backup: bool = True,
                         skip_existing: bool = True) -> Dict:
        """Process all files in a directory"""
        
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
        
        # Collect files
        files_to_process = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                ext = Path(filepath).suffix.lower()
                
                # Skip if already in target format and skip_existing is True
                if skip_existing and re.match(r'\d{8}_\d{3}\.(jpg|jpeg|png|mp3|mp4|pdf|txt)$', filename):
                    print(f"Skipping already renamed file: {filename}")
                    continue
                
                # Filter by extensions if specified
                if file_extensions:
                    if ext not in file_extensions:
                        continue
                elif ext not in self.supported_extensions:
                    continue
                
                files_to_process.append(filepath)
        
        print(f"Found {len(files_to_process)} files to process...")
        
        # Extract dates and sort
        files_with_dates = []
        for filepath in files_to_process:
            file_date = self.get_file_date(filepath)
            category = self.detect_file_category(filepath)
            files_with_dates.append((file_date, filepath, category))
            print(f"{os.path.basename(filepath)} -> {file_date.strftime('%Y-%m-%d %H:%M:%S')} ({category})")
        
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
        
        for file_date, original_path, category in files_with_dates:
            try:
                # Get sequence number for this date
                date_str = file_date.strftime('%Y%m%d')
                if date_str not in date_sequences:
                    date_sequences[date_str] = 1
                else:
                    date_sequences[date_str] += 1
                
                sequence = date_sequences[date_str]
                
                # Generate new filename
                new_filename = self.generate_new_filename(
                    file_date, sequence, naming_pattern, original_path, category
                )
                
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
                    results['details'].append({
                        'original': original_path,
                        'new': new_filepath,
                        'date': file_date.isoformat(),
                        'category': category
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
                    
                    # Rename file
                    if original_path != new_filepath:
                        shutil.move(original_path, new_filepath)
                        print(f"Renamed: {os.path.basename(original_path)} -> {new_filename}")
                    else:
                        print(f"No change needed: {new_filename}")
                    
                    results['processed'] += 1
                
            except Exception as e:
                print(f"Error processing {original_path}: {e}")
                results['errors'] += 1
        
        return results

    def generate_report(self, directory: str, results: Dict, output_file: str = None):
        """Generate a processing report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'directory': directory,
            'summary': {
                'processed': results['processed'],
                'errors': results['errors'],
                'skipped': results['skipped']
            },
            'files': results.get('details', [])
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved to: {output_file}")
        else:
            print(json.dumps(report, indent=2))

def main():
    parser = argparse.ArgumentParser(description='Simple batch file renamer by date')
    parser.add_argument('directory', help='Directory to process')
    parser.add_argument('-o', '--output', help='Output directory (default: same as input)')
    parser.add_argument('-p', '--pattern', default='date_sequence', 
                       choices=['date_sequence', 'date_time_sequence', 'year_month_sequence', 'category_date_sequence'],
                       help='Naming pattern to use')
    parser.add_argument('-e', '--extensions', nargs='+',
                       help='File extensions to process (e.g., .jpg .png .mp3)')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip creating backup of original files')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without applying them')
    parser.add_argument('--include-existing', action='store_true',
                       help='Include files that appear to be already renamed')
    parser.add_argument('--report', help='Save detailed report to JSON file')
    
    args = parser.parse_args()
    
    # Convert extensions to lowercase with dots
    extensions = None
    if args.extensions:
        extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                     for ext in args.extensions]
    
    renamer = SimpleBatchRenamer()
    
    try:
        results = renamer.process_directory(
            directory=args.directory,
            output_dir=args.output,
            naming_pattern=args.pattern,
            file_extensions=extensions,
            dry_run=args.dry_run,
            backup=not args.no_backup,
            skip_existing=not args.include_existing
        )
        
        print(f"\n{'=' * 50}")
        print(f"{'DRY RUN ' if args.dry_run else ''}RESULTS:")
        print(f"{'=' * 50}")
        print(f"Processed: {results['processed']}")
        print(f"Errors: {results['errors']}")
        print(f"Skipped: {results['skipped']}")
        
        if args.dry_run:
            print(f"\nTo apply these changes, run without --dry-run")
        
        # Generate report if requested
        if args.report:
            renamer.generate_report(args.directory, results, args.report)
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
