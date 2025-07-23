"""
File Processing Module
Handles individual file conversion and batch processing operations.
"""

import codecs
from pathlib import Path

from html_filter import md_to_filtered_html
from utf8_sanitizer import read_file_with_encoding_fallback, force_utf8_and_sanitize, force_utf8_entire_directory


def process_single_file(input_path, output_path):
    """Process a single Markdown file and convert it to filtered HTML."""
    try:
        # Read file with encoding fallback
        md_content, source_encoding = read_file_with_encoding_fallback(input_path)
        if source_encoding != 'utf-8':
            print(f"  Note: Read {input_path.name} using {source_encoding} encoding")
        
        # Convert Markdown to filtered HTML
        html_content = md_to_filtered_html(md_content)
        
        # Apply UTF-8 sanitization for HTML content
        html_content = force_utf8_and_sanitize(html_content, is_html=True)
        
        # Write to output file in UTF-8
        with codecs.open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True, None
    except Exception as e:
        return False, str(e)


def batch_convert_directory(input_dir, output_dir):
    """Convert all Markdown files in a directory to filtered HTML."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Validate input directory
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return
    
    if not input_path.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        return
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all Markdown files
    md_files = list(input_path.glob('*.md'))
    
    if not md_files:
        print(f"No Markdown files found in '{input_dir}'.")
        return
    
    print(f"Found {len(md_files)} Markdown files to convert...")
    
    # Process each file
    successful = 0
    failed = 0
    
    for md_file in md_files:
        output_filename = md_file.stem + '.html'
        output_file_path = output_path / output_filename
        
        print(f"Converting: {md_file.name} -> {output_filename}")
        
        success, error = process_single_file(md_file, output_file_path)
        
        if success:
            successful += 1
            print(f"  ✓ Successfully converted")
        else:
            failed += 1
            print(f"  ✗ Failed to convert: {error}")
    
    print(f"\nConversion complete!")
    print(f"Successfully converted: {successful} files")
    print(f"Failed to convert: {failed} files")
    
    # Apply UTF-8 encoding and sanitization to all output files
    if successful > 0:
        print(f"\nApplying UTF-8 encoding and sanitization to output directory...")
        sanitized_files = force_utf8_entire_directory(output_path)
        print(f"Processed and sanitized: {sanitized_files} files")
    
    print(f"\nHTML files saved in: {output_path}")
