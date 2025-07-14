# WordPress Image Compressor

  A Python script that recursively compresses and optimizes images in WordPress upload directories while preserving file
  paths, names, and transparency.

  ## Features

  - **JPEG Compression**: Applies quality-based compression with configurable settings
  - **PNG Optimization**: Lossless optimization while preserving transparency
  - **WebP Support**: Quality-based compression for WebP files
  - **Smart Resizing**: Automatically resizes oversized images while maintaining aspect ratio
  - **Transparency Preservation**: Keeps PNG and WebP transparency intact
  - **Batch Processing**: Recursively processes entire directory trees
  - **Dry Run Mode**: Preview changes without modifying files
  - **Detailed Statistics**: Shows file sizes, savings, and compression percentages
  - **Safe Operation**: Requires confirmation before making changes

  ## Requirements

  - Python 3.6+
  - Pillow (PIL)

  ## Installation

  1. Clone this repository:
  ```bash
  git clone https://github.com/yourusername/wp-image-compressor.git
  cd wp-image-compressor

  2. Install dependencies:
  pip install Pillow

  Usage

  Basic Usage

  python wp_image_compressor.py /path/to/wp-content/uploads

  Advanced Options

  # Custom quality and dimensions
  python wp_image_compressor.py /path/to/uploads --quality 75 --max-width 1200

  # Dry run (preview without changes)
  python wp_image_compressor.py /path/to/uploads --dry-run

  # Full example with all options
  python wp_image_compressor.py /var/www/wp-content/uploads --quality 80 --max-width 1600 --max-height 900

  Command Line Options

  | Option       | Short | Description                             | Default |
  |--------------|-------|-----------------------------------------|---------|
  | --quality    | -q    | JPEG quality (1-100)                    | 85      |
  | --max-width  | -w    | Maximum width in pixels                 | 1920    |
  | --max-height |       | Maximum height in pixels                | 1080    |
  | --dry-run    | -d    | Preview changes without modifying files | False   |

  How It Works

  File Processing

  - JPEG (.jpg, .jpeg): Converts to RGB, applies quality compression, and resizes if needed
  - PNG (.png): Preserves transparency, applies lossless optimization, and resizes if needed
  - WebP (.webp): Preserves original color mode, applies quality compression, and resizes if needed
  - Other formats: Skipped to preserve animations and special properties

  Safety Features

  - Backup warning before processing
  - Confirmation prompt for destructive operations
  - Dry run mode for safe preview
  - Detailed progress reporting
  - Error handling with descriptive messages

  Example Output

  Processing images in: /var/www/wp-content/uploads
  Quality: 85%, Max dimensions: 1920x1080
  ------------------------------------------------------------
  Processing: 2023/01/image1.jpg (2.3MB) -> 890.5KB (saved 1.4MB, 61.2%)
  Processing: 2023/01/logo.png (156.2KB) -> 98.7KB (saved 57.5KB, 36.8%)
  Skipping unsupported format: .gif

  ============================================================
  SUMMARY
  ============================================================
  Total files found: 245
  Successfully processed: 243
  Failed: 2
  Original total size: 45.2MB
  Compressed total size: 18.7MB
  Total savings: 26.5MB (58.6%)

  Important Notes

  - Always backup your images before running the script
  - PNG transparency is preserved - no white backgrounds added
  - File paths and names remain unchanged
  - Original EXIF orientation is respected
  - The script modifies images in-place

  Contributing

  1. Fork the repository
  2. Create your feature branch (git checkout -b feature/amazing-feature)
  3. Commit your changes (git commit -m 'Add amazing feature')
  4. Push to the branch (git push origin feature/amazing-feature)
  5. Open a Pull Request

  License

  This project is licensed under the MIT License - see the LICENSE file for details.

  Disclaimer

  This script modifies image files permanently. Always ensure you have proper backups before running it on important
  data.
