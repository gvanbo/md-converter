"""
Configuration Module
Central configuration settings for the Markdown to HTML converter.
"""

# Markdown processing configuration
MARKDOWN_EXTENSIONS = [
    'tables',        # Table support
    'fenced_code',   # Code block support
    'codehilite',    # Syntax highlighting (filtered out later)
    'toc',           # Table of contents
    'attr_list'      # Custom attributes on elements
]

# File processing configuration
SUPPORTED_INPUT_EXTENSIONS = ['.md', '.markdown', '.txt']
OUTPUT_EXTENSION = '.html'

# Binary file extensions to skip during UTF-8 processing
BINARY_FILE_EXTENSIONS = [
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff',
    '.zip', '.rar', '.7z', '.tar', '.gz',
    '.mp4', '.avi', '.mov', '.wmv', '.flv',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.exe', '.dll', '.so', '.dylib'
]

# Encoding fallback order
ENCODING_FALLBACKS = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']

# HTML processing configuration
HTML_FILE_EXTENSIONS = ['.html', '.htm']

# Default directory names
DEFAULT_INPUT_DIR = 'md-downloads'
DEFAULT_OUTPUT_DIR = 'converted-html-descriptions'

# Processing options
ENABLE_PROGRESS_REPORTING = True
ENABLE_UTF8_SANITIZATION = True
ENABLE_CHARACTER_FILTERING = True

# Character replacements for sanitization
CHARACTER_REPLACEMENTS = {
    # Smart quotes to straight quotes
    '"': '"',
    '"': '"',
    ''': "'",
    ''': "'",
    
    # Dashes to hyphens
    '–': '-',  # En dash
    '—': '-',  # Em dash
    
    # Special characters
    '…': '...',  # Ellipsis
    '\xa0': ' ',  # Non-breaking space
    
    # Unicode code points
    '\u201c': '"',   # Left double quotation mark
    '\u201d': '"',   # Right double quotation mark
    '\u2018': "'",   # Left single quotation mark
    '\u2019': "'",   # Right single quotation mark
    '\u2013': '-',   # En dash
    '\u2014': '-',   # Em dash
    '\u2026': '...',  # Horizontal ellipsis
    
    # Common encoding artifacts
    '�': '"',
    'â€œ': '"',
    'â€': '"',
    'â€™': "'",
    'â€˜': "'",
    'â€"': '-',
    'â€"': '-',
    'â€¦': '...',
    
    # Problematic characters
    '*': '',  # Remove asterisks that can cause formatting issues
}

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
