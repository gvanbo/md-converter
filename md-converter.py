import os
import subprocess
import sys
import codecs
from pathlib import Path

# Install required dependencies
required_packages = ['markdown', 'beautifulsoup4']
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        print(f"The '{package}' library is not installed. Installing it now...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

import markdown
from bs4 import BeautifulSoup, NavigableString

# Allowed tags and their allowed attributes
ALLOWED_TAGS = {
    'h2': [],
    'h3': [],
    'p': [],
    'strong': [],
    'em': [],
    'quote': ['cite', 'author'],  # Custom attributes for <quote>
    'table': ['border', 'cellpadding', 'cellspacing'],
    'thead': [],
    'tbody': [],
    'tr': [],
    'th': [],
    'td': [],
}

# Mapping disallowed tags to allowed ones
TAG_REPLACEMENTS = {
    'h1': 'h2',
    'h4': 'h3',
    'h5': 'h3',
    'h6': 'p',
    'ul': 'p',
    'ol': 'p',
    'li': 'p',
    'blockquote': 'quote',  # Custom mapping to <quote>
    'code': 'em',
    'pre': 'p',
    'span': 'p',
    'div': 'p',
    'a': 'em',
    'img': 'p',
    'br': 'p',  # Convert line breaks to paragraphs
}

def force_utf8_and_sanitize(content, is_html=False):
    """
    Force UTF-8 encoding and sanitize problematic characters.
    If is_html=True, applies additional HTML-specific sanitization.
    """
    # For HTML files, remove problematic characters for print environments
    if is_html:
        # Replace non-breaking spaces (\xa0) with regular spaces
        content = content.replace('\xa0', ' ')
        
        # Replace smart quotes with straight quotes
        content = content.replace('"', '"').replace('"', '"')
        content = content.replace(''', '\'').replace(''', '\'')
        
        # Replace en dashes and em dashes with hyphens
        content = content.replace('–', '-').replace('—', '-')
        
        # Replace ellipsis with three dots
        content = content.replace('…', '...')
        
        # Replace common corrupted characters and encoding artifacts
        content = content.replace('�', '"')  # Common corruption of smart quotes
        content = content.replace('â€œ', '"')  # UTF-8 encoding issue for left double quote
        content = content.replace('â€', '"')   # UTF-8 encoding issue for right double quote
        content = content.replace('â€™', "'")  # UTF-8 encoding issue for right single quote
        content = content.replace('â€˜', "'")  # UTF-8 encoding issue for left single quote
        content = content.replace('â€"', '-')  # UTF-8 encoding issue for en dash
        content = content.replace('â€"', '-')  # UTF-8 encoding issue for em dash
        content = content.replace('â€¦', '...') # UTF-8 encoding issue for ellipsis
        
        # Replace other common problematic Unicode characters
        content = content.replace('\u201c', '"')  # Left double quotation mark
        content = content.replace('\u201d', '"')  # Right double quotation mark
        content = content.replace('\u2018', "'")  # Left single quotation mark
        content = content.replace('\u2019', "'")  # Right single quotation mark
        content = content.replace('\u2013', '-')  # En dash
        content = content.replace('\u2014', '-')  # Em dash
        content = content.replace('\u2026', '...') # Horizontal ellipsis
        
        # Remove asterisk characters that can cause formatting issues
        content = content.replace('*', '')
    
    return content

def read_file_with_encoding_fallback(file_path):
    """
    Read a file with UTF-8, falling back to other encodings if needed.
    Returns the content as a string.
    """
    encodings = ['utf-8', 'cp1252', 'latin-1']
    
    for encoding in encodings:
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading {file_path} with {encoding}: {e}")
            continue
    
    raise Exception(f"Could not read {file_path} with any supported encoding")
    """Filter HTML content to only include allowed tags and attributes."""
    soup = BeautifulSoup(html, 'html.parser')

    # Process all tags in the document
    for tag in soup.find_all(True):
        if tag.name in ALLOWED_TAGS:
            # Only retain allowed attributes
            allowed_attrs = ALLOWED_TAGS[tag.name]
            attrs_to_remove = [attr for attr in tag.attrs if attr not in allowed_attrs]
            for attr in attrs_to_remove:
                del tag.attrs[attr]
        elif tag.name in TAG_REPLACEMENTS:
            # Replace with mapped tag
            new_tag_name = TAG_REPLACEMENTS[tag.name]
            tag.name = new_tag_name
            tag.attrs = {}  # Strip all attributes for replaced tags
        else:
            # Replace unsupported tag with <p> preserving text content
            replacement = soup.new_tag("p")
            
            # Preserve all text content from the tag
            text_content = tag.get_text()
            if text_content.strip():
                replacement.string = text_content
            
            tag.replace_with(replacement)

    # Clean up empty paragraphs and normalize whitespace
    for p_tag in soup.find_all('p'):
        if not p_tag.get_text().strip():
            p_tag.decompose()
        else:
            # Normalize whitespace
            if p_tag.string:
                p_tag.string = ' '.join(p_tag.string.split())

    return str(soup)

def md_to_filtered_html(md_text):
    """Convert Markdown text to filtered HTML."""
    # Use comprehensive extensions for better Markdown support
    html = markdown.markdown(
        md_text, 
        extensions=['tables', 'fenced_code', 'codehilite', 'toc', 'attr_list']
    )
    return filter_html(html)

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

def force_utf8_entire_directory(directory):
    """
    Apply UTF-8 encoding and sanitization to all files in the output directory.
    This is the integrated version of the force-utf8.py functionality.
    """
    processed_files = 0
    
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Skip binary files
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.zip', '.mp4', '.pdf')):
                continue
                
            try:
                # Read with encoding fallback
                content, encoding = read_file_with_encoding_fallback(file_path)
                
                # Apply sanitization (HTML-specific for .html/.htm files)
                is_html = file_name.lower().endswith(('.html', '.htm'))
                content = force_utf8_and_sanitize(content, is_html=is_html)
                
                # Write back in UTF-8
                with codecs.open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                processed_files += 1
                
            except Exception as e:
                print(f"  Warning: Could not process {file_path}: {e}")
    
    return processed_files
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

def main():
    """Main function to handle command line usage or default batch processing."""
    # Default directories
    script_dir = Path(__file__).parent
    default_input_dir = script_dir / 'md-downloads'
    default_output_dir = script_dir / 'converted-html-descriptions'
    
    # Check for command line arguments
    if len(sys.argv) == 1:
        # No arguments - use default directories
        input_dir = default_input_dir
        output_dir = default_output_dir
    elif len(sys.argv) == 3:
        # Two arguments - input and output directories
        input_dir = Path(sys.argv[1])
        output_dir = Path(sys.argv[2])
    else:
        print("Usage:")
        print("  python md-converter.py                    # Use default directories")
        print("  python md-converter.py <input_dir> <output_dir>  # Specify directories")
        sys.exit(1)
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print("-" * 50)
    
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


def main():
    """Main function to handle command line usage or default batch processing."""
    # Default directories
    script_dir = Path(__file__).parent
    default_input_dir = script_dir / 'md-downloads'
    default_output_dir = script_dir / 'converted-html-descriptions'
    
    # Check for command line arguments
    if len(sys.argv) == 1:
        # No arguments - use default directories
        input_dir = default_input_dir
        output_dir = default_output_dir
    elif len(sys.argv) == 3:
        # Two arguments - input and output directories
        input_dir = Path(sys.argv[1])
        output_dir = Path(sys.argv[2])
    else:
        print("Usage:")
        print("  python md-converter.py                    # Use default directories")
        print("  python md-converter.py <input_dir> <output_dir>  # Specify directories")
        sys.exit(1)
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print("-" * 50)
    
    batch_convert_directory(input_dir, output_dir)


if __name__ == "__main__":
    main()
