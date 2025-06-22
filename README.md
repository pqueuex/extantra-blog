# Extantra Blog

A minimal, modern media/blog site with dynamic galleries and a retro aesthetic.

## Features

- **Multi-Media Galleries**: Music, 3D models, drawings, photos, and videos
- **Custom Video Player**: Auto-play, playlist functionality, and metadata display
- **Hidden Blog Interface**: Triple-click the logo to access the admin panel
- **Batch Processing**: Scripts for media conversion and metadata generation
- **Retro Aesthetic**: Pixel-perfect fonts and minimal design
- **Search Engine Blocked**: Not discoverable by search engines

## Gallery Types

- **Music**: Audio player with track listing
- **3D Models**: Interactive 3D viewer for GLB files
- **Drawings**: WebP optimized drawing gallery
- **Photos**: Chronologically sorted photo dump
- **Videos**: Custom video player with playlist support

## Technical Features

- Pure HTML/CSS/JavaScript (no frameworks)
- Responsive design
- File:// and HTTP(S) compatibility
- Metadata databases for all media types
- Batch processing scripts for media organization

## File Structure

```
├── index.html              # Main blog page
├── photos.html            # Photo gallery
├── drawings.html          # Drawings gallery
├── 3d-models.html         # 3D model viewer
├── video.html            # Video player
├── music.html            # Music player
├── styles.css            # Site-wide styles
├── robots.txt           # Search engine blocking
├── *-database.json      # Metadata databases
├── batch_*.py          # Media processing scripts
└── [media folders]/    # Organized media files
```

## Admin Interface

Access the blog post creation interface by triple-clicking the site logo. Create posts with:
- Title and excerpt
- Date and tags
- Rich text content
- Draft/publish states

## Media Processing

Includes batch scripts for:
- Photo renaming and optimization
- Drawing conversion to WebP
- Video compression and metadata extraction
- Chronological organization by date

## Setup

1. Clone the repository
2. Open `index.html` in a web browser
3. For batch processing, install Python dependencies:
   ```bash
   pip install -r batch_converter_requirements.txt
   ```

## Note

This site is intentionally designed to be undiscoverable by search engines and maintains a minimal, retro aesthetic throughout.
