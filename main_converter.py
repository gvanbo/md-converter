#!/usr/bin/env python3
"""
Markdown to HTML Converter
Main application entry point with command line interface.

This script converts Markdown files to clean, filtered HTML suitable for
websites and Moodle Learning Management Systems.

Usage:
    python md-converter.py                           # Use default directories
    python md-converter.py <input_dir> <output_dir>  # Specify custom directories

Author: Auto-generated modular converter
Version: 2.0
"""

import sys
from pathlib import Path

# Import our modules
from dependency_manager import initialize_dependencies
from file_processor import batch_convert_directory


def print_usage():
    """Print usage instructions."""
    print("Markdown to HTML Converter v2.0")
    print("=" * 40)
    print()
    print("Usage:")
    print("  python md-converter.py                           # Use default directories")
    print("  python md-converter.py <input_dir> <output_dir>  # Specify directories")
    print()
    print("Default directories:")
    print("  Input:  ./md-downloads/")
    print("  Output: ./converted-html-descriptions/")
    print()
    print("Features:")
    print("  • Converts Markdown (.md) files to clean HTML")
    print("  • Filters HTML to allowed tags only")
    print("  • Automatic UTF-8 encoding and character sanitization")
    print("  • Moodle and web-compatible output")
    print("  • Batch processing with progress reporting")


def validate_arguments():
    """Validate and process command line arguments."""
    script_dir = Path(__file__).parent
    
    if len(sys.argv) == 1:
        # No arguments - use default directories
        input_dir = script_dir / 'md-downloads'
        output_dir = script_dir / 'converted-html-descriptions'
        
    elif len(sys.argv) == 3:
        # Two arguments - input and output directories
        input_dir = Path(sys.argv[1])
        output_dir = Path(sys.argv[2])
        
    elif len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help', 'help']:
        # Help requested
        print_usage()
        sys.exit(0)
        
    else:
        print("Error: Invalid number of arguments.")
        print()
        print_usage()
        sys.exit(1)
    
    return input_dir, output_dir


def main():
    """Main function to orchestrate the conversion process."""
    try:
        # Initialize dependencies
        initialize_dependencies()
        
        # Process command line arguments
        input_dir, output_dir = validate_arguments()
        
        # Display configuration
        print("Configuration:")
        print(f"  Input directory:  {input_dir}")
        print(f"  Output directory: {output_dir}")
        print("-" * 50)
        
        # Perform the conversion
        batch_convert_directory(input_dir, output_dir)
        
        print("\n" + "="*50)
        print("Conversion process completed successfully!")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n\nConversion cancelled by user.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nFor help, run: python md-converter.py --help")
        sys.exit(1)


if __name__ == "__main__":
    main()
