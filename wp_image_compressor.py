#!/usr/bin/env python3
"""
WordPress Image Compression Script
Recursively compresses all images in WordPress upload folders
"""

import os
import sys
from PIL import Image, ImageOps
import argparse

def compress_image(image_path, quality=85, max_width=1920, max_height=1080):
    """
    Compress an image while maintaining aspect ratio.
    Returns the final file path if successful, False otherwise.
    """
    try:
        with Image.open(image_path) as img:
            ext = os.path.splitext(image_path)[1].lower()
            
            # Handle JPEGs - convert to RGB and apply compression
            if ext in ['.jpg', '.jpeg']:
                # Convert to RGB if needed (handles transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                        img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if needed
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Auto-orient
                img = ImageOps.exif_transpose(img)
                
                img.save(image_path, 'JPEG', quality=quality, optimize=True)
                return image_path
            
            # Handle PNGs - preserve transparency, only resize and optimize
            elif ext == '.png':
                # Resize if needed (preserve original mode for transparency)
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Auto-orient
                img = ImageOps.exif_transpose(img)
                
                img.save(image_path, 'PNG', optimize=True)
                return image_path
            
            # Handle WebP - preserve original mode
            elif ext == '.webp':
                # Resize if needed
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Auto-orient
                img = ImageOps.exif_transpose(img)
                
                img.save(image_path, 'WEBP', quality=quality, optimize=True)
                return image_path
            
            # Skip other formats (GIF, etc.) to preserve animations and transparency
            else:
                print(f"Skipping unsupported format: {ext}")
                return image_path
    except Exception as e:
        print(f"Error compressing {image_path}: {e}")
        return False

def get_file_size(file_path):
    return os.path.getsize(file_path)

def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def compress_wordpress_images(upload_path, quality=85, max_width=1920, max_height=1080, dry_run=False):
    """
    Compress all images in WordPress upload directory.
    """
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    total_files = 0
    processed = 0
    orig_size = 0
    comp_size = 0

    print(f"{'DRY RUN: ' if dry_run else ''}Processing images in: {upload_path}")
    print(f"Quality: {quality}%, Max dimensions: {max_width}x{max_height}")
    print("-" * 60)

    for root, _, files in os.walk(upload_path):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            if ext in image_exts:
                total_files += 1
                size_before = get_file_size(file_path)
                orig_size += size_before
                rel_path = os.path.relpath(file_path, upload_path)
                if dry_run:
                    print(f"Would process: {rel_path} ({format_size(size_before)})")
                else:
                    print(f"Processing: {rel_path} ({format_size(size_before)})", end=" -> ")
                    result = compress_image(file_path, quality, max_width, max_height)
                    if result:
                        size_after = get_file_size(result)
                        comp_size += size_after
                        savings = size_before - size_after
                        percent = (savings / size_before) * 100 if size_before > 0 else 0
                        print(f"{format_size(size_after)} (saved {format_size(savings)}, {percent:.1f}%)")
                        processed += 1
                    else:
                        print("FAILED")
                        comp_size += size_before

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files found: {total_files}")
    if not dry_run:
        print(f"Successfully processed: {processed}")
        print(f"Failed: {total_files - processed}")
        print(f"Original total size: {format_size(orig_size)}")
        print(f"Compressed total size: {format_size(comp_size)}")
        if orig_size > 0:
            total_savings = orig_size - comp_size
            percent = (total_savings / orig_size) * 100
            print(f"Total savings: {format_size(total_savings)} ({percent:.1f}%)")

def main():
    parser = argparse.ArgumentParser(
        description="Compress images in WordPress upload directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python compress_wp_images.py /var/www/wp-content/uploads
  python compress_wp_images.py /var/www/wp-content/uploads --quality 75 --max-width 1200
  python compress_wp_images.py /var/www/wp-content/uploads --dry-run
        """
    )
    parser.add_argument('upload_path', help='Path to WordPress uploads directory')
    parser.add_argument('--quality', '-q', type=int, default=85, help='JPEG quality (1-100, default: 85)')
    parser.add_argument('--max-width', '-w', type=int, default=1920, help='Maximum width in pixels (default: 1920)')
    parser.add_argument('--max-height', type=int, default=1080, help='Maximum height in pixels (default: 1080)')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Show what would be processed without making changes')
    args = parser.parse_args()

    # Validate arguments
    if not os.path.exists(args.upload_path):
        print(f"Error: Upload path does not exist: {args.upload_path}")
        sys.exit(1)
    if not os.path.isdir(args.upload_path):
        print(f"Error: Upload path is not a directory: {args.upload_path}")
        sys.exit(1)
    if not 1 <= args.quality <= 100:
        print("Error: Quality must be between 1 and 100")
        sys.exit(1)
    if args.max_width <= 0 or args.max_height <= 0:
        print("Error: Max width and height must be positive")
        sys.exit(1)

    if not args.dry_run:
        print("WARNING: This will modify your images permanently!")
        print("Make sure you have a backup before proceeding.")
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    compress_wordpress_images(
        args.upload_path,
        args.quality,
        args.max_width,
        args.max_height,
        args.dry_run
    )

if __name__ == "__main__":
    main()