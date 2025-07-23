"""
UTF-8 Sanitization Module
Handles encoding normalization and character sanitization for HTML files.
"""

import os
import codecs


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
    Returns the content as a string and the encoding used.
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
