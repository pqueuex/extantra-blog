#!/usr/bin/env python3
"""
Batch Processing Demo Script
Demonstrates the capabilities of the batch file processing tools
"""

import os
import subprocess
import json
from pathlib import Path

def run_demo():
    """Run demonstration of batch processing features"""
    
    print("🎯 BATCH FILE PROCESSING DEMO")
    print("=" * 50)
    
    # Create a test directory with sample files
    demo_dir = "/tmp/batch_demo"
    os.makedirs(demo_dir, exist_ok=True)
    
    # Create some test files with various naming patterns
    test_files = [
        "IMG_20230815_143052.jpg",
        "PXL_20240125_043347823.MP.jpg", 
        "Screenshot_2024-03-15_at_2.30.45_PM.png",
        "vacation_photo.jpeg",
        "DSC00887.JPG",
        "document_scan.pdf",
        "audio_recording.mp3",
        "presentation.pptx",
        "random_image.png",
        "2024-01-01_NewYear.jpg"
    ]
    
    print(f"📁 Creating demo files in {demo_dir}")
    for filename in test_files:
        filepath = os.path.join(demo_dir, filename)
        with open(filepath, 'w') as f:
            f.write(f"Demo file: {filename}")
    
    print(f"✅ Created {len(test_files)} test files")
    print()
    
    # Demo 1: Basic dry run
    print("🔍 DEMO 1: Basic Dry Run Analysis")
    print("-" * 30)
    cmd = [
        "python3", "/Users/jj/extantra-blog/simple_batch_renamer.py",
        demo_dir, "--dry-run"
    ]
    subprocess.run(cmd)
    print()
    
    # Demo 2: Specific file types only
    print("🖼️  DEMO 2: Images Only with Date-Time Pattern")
    print("-" * 40)
    cmd = [
        "python3", "/Users/jj/extantra-blog/simple_batch_renamer.py",
        demo_dir, "--dry-run", 
        "--extensions", ".jpg", ".jpeg", ".png",
        "--pattern", "date_time_sequence"
    ]
    subprocess.run(cmd)
    print()
    
    # Demo 3: Category-based naming
    print("📂 DEMO 3: Category-Based Naming")
    print("-" * 30)
    cmd = [
        "python3", "/Users/jj/extantra-blog/simple_batch_renamer.py",
        demo_dir, "--dry-run",
        "--pattern", "category_date_sequence"
    ]
    subprocess.run(cmd)
    print()
    
    # Demo 4: Generate report
    print("📊 DEMO 4: Generate Processing Report")
    print("-" * 35)
    report_file = os.path.join(demo_dir, "processing_report.json")
    cmd = [
        "python3", "/Users/jj/extantra-blog/simple_batch_renamer.py",
        demo_dir, "--dry-run",
        "--report", report_file
    ]
    subprocess.run(cmd)
    
    # Show report contents
    if os.path.exists(report_file):
        with open(report_file) as f:
            report = json.load(f)
        print(f"\n📄 Report saved to: {report_file}")
        print(f"   Summary: {report['summary']}")
        print(f"   Files processed: {len(report['files'])}")
    print()
    
    # Show available options
    print("⚙️  AVAILABLE OPTIONS:")
    print("-" * 20)
    print("Naming Patterns:")
    print("  • date_sequence (default): 20240125_001.jpg")
    print("  • date_time_sequence: 20240125_143052_001.jpg") 
    print("  • year_month_sequence: 2024-01_001.jpg")
    print("  • category_date_sequence: photo_20240125_001.jpg")
    print()
    print("File Type Filters:")
    print("  • --extensions .jpg .png .mp4 (specific types)")
    print("  • Auto-detects: images, audio, video, documents")
    print()
    print("Safety Features:")
    print("  • --dry-run (preview changes)")
    print("  • --no-backup (skip backup creation)")
    print("  • --report file.json (detailed logging)")
    print("  • Collision detection (skips existing files)")
    print()
    
    # Cleanup
    print("🧹 Cleaning up demo files...")
    import shutil
    shutil.rmtree(demo_dir)
    print("✅ Demo completed!")

def show_real_world_examples():
    """Show real-world usage examples from the actual project"""
    
    print("\n🌍 REAL-WORLD EXAMPLES FROM THIS PROJECT")
    print("=" * 45)
    
    print("📸 Photos Directory (88 files already processed):")
    print("   Before: PXL_20240125_043347823.MP.jpg, IMG_1504.jpg, DSC00887.JPG")
    print("   After:  20240125_001.jpg, 20230601_001.jpg, 20241215_001.jpg")
    print()
    
    print("🎨 Drawings Directory (29 mixed files):")
    print("   Command: python3 simple_batch_renamer.py drawings --dry-run")
    print("   Detects: PXL camera files, screenshots, scanned images, illustrations")
    print("   Groups by date with sequential numbering within each day")
    print()
    
    print("🎵 Potential Audio Processing:")
    print("   Command: python3 batch_convert_rename.py audio --convert .mp3 --quality 192")
    print("   Features: Metadata extraction, format conversion, date-based organization")
    print()
    
    print("📁 Mixed Media Batch:")
    print("   Command: python3 simple_batch_renamer.py . --extensions .jpg .mp4 .pdf")
    print("   Result: Organizes photos, videos, and documents by chronological date")

if __name__ == "__main__":
    try:
        run_demo()
        show_real_world_examples()
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
