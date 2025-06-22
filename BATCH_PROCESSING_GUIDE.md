# Batch File Converter and Renamer

This toolkit provides two powerful scripts for batch processing files with date-based chronological renaming:

## Scripts Overview

### 1. `simple_batch_renamer.py` - Standard Library Only
- **No dependencies required** - works with Python standard library
- Renames files by date with chronological numbering
- Supports intelligent date extraction from filenames and file metadata
- Perfect for quick renaming tasks

### 2. `batch_convert_rename.py` - Enhanced Features
- **Requires additional packages** (see requirements below)
- File format conversion (images, audio, video)
- EXIF metadata extraction from images
- Audio metadata extraction
- Advanced date detection methods

## Installation

### Basic Version (simple_batch_renamer.py)
No installation required - uses Python standard library only.

### Enhanced Version (batch_convert_rename.py)
```bash
pip install Pillow mutagen ffmpeg-python
# or
pip install -r batch_converter_requirements.txt
```

## Usage Examples

### Basic File Renaming

```bash
# Dry run to preview changes
python3 simple_batch_renamer.py /path/to/files --dry-run

# Rename all supported files in a directory
python3 simple_batch_renamer.py /path/to/files

# Rename only specific file types
python3 simple_batch_renamer.py /path/to/files --extensions .jpg .png .mp4

# Use different naming pattern
python3 simple_batch_renamer.py /path/to/files --pattern date_time_sequence

# Output to different directory
python3 simple_batch_renamer.py /path/to/files --output /path/to/renamed

# Skip backup creation
python3 simple_batch_renamer.py /path/to/files --no-backup

# Generate detailed report
python3 simple_batch_renamer.py /path/to/files --report results.json
```

### Advanced Features with Enhanced Version

```bash
# Convert images to different format while renaming
python3 batch_convert_rename.py /path/to/images --convert .webp

# Process only specific file types
python3 batch_convert_rename.py /path/to/files --types image audio

# Use custom quality for image conversion
python3 batch_convert_rename.py /path/to/images --convert .jpg --quality 85

# Different naming patterns
python3 batch_convert_rename.py /path/to/files --pattern category_date_sequence
```

## Naming Patterns

- **`date_sequence`**: `20240125_001.jpg` (default)
- **`date_time_sequence`**: `20240125_143052_001.jpg`
- **`year_month_sequence`**: `2024-01_001.jpg`
- **`category_date_sequence`**: `photo_20240125_001.jpg`

## Date Detection Methods

The scripts intelligently detect dates from multiple sources:

1. **EXIF metadata** (images) - most accurate
2. **Audio metadata** (enhanced version only)
3. **Filename patterns**:
   - `PXL_20240125_043347823.MP.jpg` (Google Pixel)
   - `IMG_20240125_043347.jpg` (common camera format)
   - `Screenshot 2024-01-25 at 04.33.47.png`
   - `20240125_043347.jpg`
   - `2024-01-25_04-33-47.jpg`
   - `20240125.jpg`
   - `2024-01-25.jpg`
4. **File modification time** (fallback)
5. **File creation time** (fallback)

## Features

### File Processing
- ✅ **Chronological ordering** by date extracted from multiple sources
- ✅ **Automatic backup** of original files (optional)
- ✅ **Dry run mode** to preview changes
- ✅ **Collision detection** - skips files that would overwrite existing ones
- ✅ **Progress reporting** with detailed logs
- ✅ **Error handling** - continues processing on individual file errors

### File Type Support
- 📸 **Images**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`, `.gif`
- 🎵 **Audio**: `.mp3`, `.flac`, `.m4a`, `.wav`, `.ogg`, `.aac`
- 🎬 **Video**: `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`
- 📄 **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.md`

### Smart Features
- **Skip already renamed files** (detects existing `YYYYMMDD_XXX` format)
- **Category detection** based on file extensions
- **Flexible output options** (same directory or separate output)
- **JSON reporting** for detailed processing logs

## Example Workflows

### 1. Organizing a Photo Collection
```bash
# First, preview what will happen
python3 simple_batch_renamer.py ~/Pictures/vacation --dry-run

# Then apply the changes
python3 simple_batch_renamer.py ~/Pictures/vacation --report vacation_report.json
```

### 2. Processing Mixed Media Files
```bash
# Rename only images and videos
python3 simple_batch_renamer.py ~/Downloads --extensions .jpg .png .mp4 .mov
```

### 3. Converting and Organizing Screenshots
```bash
# Convert PNG screenshots to JPEG and rename by date
python3 batch_convert_rename.py ~/Desktop/screenshots --convert .jpg --quality 90
```

### 4. Batch Processing with Detailed Logging
```bash
# Process files with detailed report and custom pattern
python3 simple_batch_renamer.py ~/Documents/scans \
  --pattern date_time_sequence \
  --report scan_processing_report.json \
  --extensions .pdf .jpg
```

## Safety Features

- **Automatic backups** of original files (can be disabled)
- **Dry run mode** to preview all changes before applying
- **Collision detection** prevents overwriting existing files
- **Error isolation** - single file errors don't stop the entire process
- **Detailed logging** of all operations

## Output Examples

### Before:
```
IMG_1504.jpg
PXL_20240625_1609379023.jpg
Screenshot_2024-03-05_at_11-41-35.png
vacation_photo.jpeg
DSC00887.JPG
```

### After (date_sequence pattern):
```
20230601_001.jpg
20240305_001.png
20240625_001.jpg
20240807_001.jpg
20241215_001.jpg
```

### After (date_time_sequence pattern):
```
20230601_120000_001.jpg
20240305_114135_001.png
20240625_160937_001.jpg
20240807_143052_001.jpg
20241215_091234_001.jpg
```

## Tips

1. **Always use dry run first** to preview changes
2. **Keep backups enabled** unless you're absolutely sure
3. **Use specific file extensions** to process only what you need
4. **Generate reports** for large batches to track what was processed
5. **Test on a small subset** before processing large collections

## Troubleshooting

- **Permission errors**: Ensure you have write access to the target directory
- **Import errors in enhanced version**: Install required packages with pip
- **Date detection issues**: Files will fall back to modification time
- **Memory usage with large files**: Process in smaller batches if needed

## Integration with Your Workflow

These scripts integrate seamlessly with your existing media management workflow:

1. **Import files** from cameras/phones to a staging directory
2. **Run batch renamer** to organize by date with chronological numbering
3. **Use the renamed files** in your galleries, databases, or other applications
4. **Archive originals** using the automatic backup feature
