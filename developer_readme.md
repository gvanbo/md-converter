# Markdown to HTML Converter - Developer Documentation

A modular Python application that converts Markdown files to sanitized HTML with strict tag filtering and UTF-8 normalization. Built with separation of concerns architecture for maintainability and extensibility.

## 🏗️ Architecture Overview

### Module Structure

```
converter/
├── md-converter.py          # Entry point, CLI interface, orchestration
├── config.py               # Centralized configuration and constants
├── dependency_manager.py   # Package installation and system checks
├── html_filter.py          # HTML processing, tag filtering, structure cleanup
├── utf8_sanitizer.py       # Encoding normalization and character sanitization
└── file_processor.py       # File I/O operations and batch processing
```

### Data Flow

```
Input .md files → Encoding Detection → Markdown Parsing → HTML Filtering → 
Character Sanitization → UTF-8 Output → Post-processing → Final HTML
```

## 🔧 Module Specifications

### `md-converter.py` - Application Controller

**Purpose**: Entry point, argument parsing, application orchestration

**Key Functions**:
- `main()` - Application entry point with error handling
- `validate_arguments()` - CLI argument processing and validation
- `print_usage()` - Help system

**Dependencies**: All other modules

**CLI Interface**:
```bash
python md-converter.py [input_dir] [output_dir]
python md-converter.py --help
```

### `config.py` - Configuration Management

**Purpose**: Centralized settings and constants

**Key Constants**:
```python
ALLOWED_TAGS = {
    'h2': [], 'h3': [], 'p': [], 'strong': [], 'em': [],
    'quote': ['cite', 'author'], 'table': [...], ...
}

TAG_REPLACEMENTS = {
    'h1': 'h2', 'h4': 'h3', 'blockquote': 'quote', ...
}

CHARACTER_REPLACEMENTS = {
    '"': '"', '"': '"', '–': '-', ...
}
```

**Customization Points**:
- HTML tag whitelist modification
- Character replacement rules
- File extension handling
- Processing options

### `dependency_manager.py` - System Requirements

**Purpose**: Automatic dependency installation and system validation

**Key Functions**:
- `initialize_dependencies()` - Main setup function
- `install_required_packages()` - Pip package installer
- `check_python_version()` - Version compatibility check

**Requirements Management**:
```python
required_packages = ['markdown', 'beautifulsoup4']
```

### `html_filter.py` - HTML Processing Core

**Purpose**: Markdown conversion and HTML tag filtering

**Key Functions**:
- `md_to_filtered_html(md_text)` - Main conversion pipeline
- `filter_html(html)` - Multi-pass HTML sanitization
- `clean_nested_paragraphs()` - Structure normalization

**Processing Pipeline**:
1. **Markdown → HTML**: Uses python-markdown with extensions
2. **List Processing**: Converts `<ul>/<ol>/<li>` to separate `<p>` tags
3. **Tag Filtering**: Applies whitelist and replacement rules
4. **Structure Cleanup**: Fixes nested paragraphs and malformed HTML
5. **Formatting Fix**: Corrects bold/italic markdown artifacts
6. **Table Normalization**: Ensures proper thead/tbody structure

**Algorithm Complexity**: O(n) where n = number of HTML nodes

### `utf8_sanitizer.py` - Character Normalization

**Purpose**: Encoding detection/conversion and character sanitization

**Key Functions**:
- `read_file_with_encoding_fallback(file_path)` - Multi-encoding file reader
- `force_utf8_and_sanitize(content, is_html)` - Character normalization
- `force_utf8_entire_directory(directory)` - Batch post-processing

**Encoding Strategy**:
```python
encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
```

**Character Sanitization Rules**:
- Smart quotes → Straight quotes
- Unicode dashes → ASCII hyphens  
- Ellipsis → Three periods
- Non-breaking spaces → Regular spaces
- Common encoding artifacts → Correct characters
- Asterisks → Removed (prevents Markdown re-interpretation)

### `file_processor.py` - File Operations

**Purpose**: File I/O, batch processing, progress reporting

**Key Functions**:
- `process_single_file(input_path, output_path)` - Individual file conversion
- `batch_convert_directory(input_dir, output_dir)` - Directory processing

**Error Handling Strategy**:
- Per-file error isolation
- Graceful degradation
- Detailed error reporting
- Continuation on individual failures

## 🧪 Testing Strategy

### Unit Testing Approach

```python
# Test each module independently
test_html_filter.py      # HTML processing logic
test_utf8_sanitizer.py   # Character sanitization
test_file_processor.py   # File operations
test_dependency_manager.py  # System setup
```

### Integration Testing

```python
# End-to-end workflow testing
def test_complete_conversion_pipeline():
    # Test: Markdown → HTML → Sanitization → Output
    
def test_encoding_edge_cases():
    # Test: Various input encodings
    
def test_malformed_markdown():
    # Test: Error handling and recovery
```

### Test Data Requirements

```
test_data/
├── input/
│   ├── standard.md           # Standard Markdown syntax
│   ├── complex_tables.md     # Advanced table formatting
│   ├── mixed_encoding.md     # CP1252 encoded file
│   ├── unicode_heavy.md      # Unicode characters and emoji
│   └── malformed.md          # Broken Markdown syntax
└── expected_output/
    ├── standard.html
    ├── complex_tables.html
    └── ...
```

## 🔄 Extension Points

### Adding New HTML Tags

1. **Update configuration**:
```python
# config.py
ALLOWED_TAGS['newtag'] = ['allowed_attr1', 'allowed_attr2']
```

2. **Optional mapping**:
```python
TAG_REPLACEMENTS['oldtag'] = 'newtag'
```

### Custom Character Sanitization

```python
# config.py
CHARACTER_REPLACEMENTS.update({
    'custom_char': 'replacement',
    '\u1234': 'normalized_version'
})
```

### New File Formats

```python
# config.py
SUPPORTED_INPUT_EXTENSIONS.extend(['.rst', '.txt', '.wiki'])

# html_filter.py - Add processing logic
def process_rst_content(content):
    # Custom processing for reStructuredText
    pass
```

### Custom Markdown Extensions

```python
# config.py
MARKDOWN_EXTENSIONS.extend(['footnotes', 'abbr', 'def_list'])
```

## 🚀 Performance Optimization

### Current Performance Characteristics

- **Memory**: O(file_size) - processes one file at a time
- **CPU**: O(n) where n = HTML nodes per file
- **I/O**: Sequential file processing

### Optimization Opportunities

1. **Parallel Processing**:
```python
from concurrent.futures import ProcessPoolExecutor

def batch_convert_parallel(file_pairs):
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_single_file, file_pairs)
```

2. **Memory Optimization**:
```python
# For very large files, implement streaming
def process_large_file_streaming(input_path, output_path):
    # Process in chunks to reduce memory footprint
```

3. **Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_html_filter(html_hash):
    # Cache filtered HTML for identical content
```

## 🔐 Security Considerations

### HTML Sanitization Security

- **XSS Prevention**: Tag whitelist blocks `<script>`, `<iframe>`, etc.
- **Attribute Filtering**: Removes `onclick`, `javascript:`, etc.
- **Content Validation**: BeautifulSoup parsing prevents HTML injection

### File System Security

- **Path Validation**: Uses pathlib.Path for safe path handling
- **Directory Traversal Prevention**: Validates input/output paths
- **File Extension Checking**: Whitelist approach for file types

### Input Validation

```python
def validate_input_safely(user_input):
    # Sanitize file paths
    safe_path = Path(user_input).resolve()
    
    # Prevent directory traversal
    if not safe_path.is_relative_to(base_dir):
        raise SecurityError("Invalid path")
```

## 🐛 Debugging Guidelines

### Common Issues and Solutions

1. **Nested Paragraph Problem**:
```python
# Debug in html_filter.py clean_nested_paragraphs()
print(f"Before cleanup: {element}")
print(f"After cleanup: {element}")
```

2. **Encoding Detection Failures**:
```python
# Debug in utf8_sanitizer.py
for encoding in encodings:
    try:
        content = file.read().decode(encoding)
        print(f"Successfully decoded with {encoding}")
        break
    except UnicodeDecodeError as e:
        print(f"Failed {encoding}: {e}")
```

3. **Character Sanitization Issues**:
```python
# Add debugging to force_utf8_and_sanitize()
def debug_char_replacement(content):
    for old, new in CHARACTER_REPLACEMENTS.items():
        count = content.count(old)
        if count > 0:
            print(f"Replacing {count} instances of '{old}' with '{new}'")
```

### Logging Implementation

```python
import logging

# Add to each module
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Usage
logger.info(f"Processing file: {filename}")
logger.warning(f"Encoding fallback used: {encoding}")
logger.error(f"Failed to process: {error}")
```

## 📊 Monitoring and Metrics

### Processing Statistics

```python
class ConversionStats:
    def __init__(self):
        self.files_processed = 0
        self.files_failed = 0
        self.encoding_fallbacks = 0
        self.characters_sanitized = 0
        self.processing_time = 0
        
    def report(self):
        # Generate detailed processing report
```

### Performance Profiling

```python
import cProfile
import pstats

def profile_conversion():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run conversion
    batch_convert_directory(input_dir, output_dir)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative').print_stats(10)
```

## 🚢 Deployment Considerations

### Production Deployment

1. **Environment Setup**:
```bash
# Requirements file
pip install -r requirements.txt

# Environment variables
export CONVERTER_INPUT_DIR="/path/to/input"
export CONVERTER_OUTPUT_DIR="/path/to/output"
```

2. **Service Configuration**:
```python
# For web service deployment
from flask import Flask, request, jsonify
from file_processor import process_single_file

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def api_convert():
    # Handle API requests
```

3. **Docker Containerization**:
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "md-converter.py"]
```

### Continuous Integration

```yaml
# .github/workflows/test.yml
name: Test Converter
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/
```

## 📚 API Reference

### Public Functions

```python
# html_filter.py
def md_to_filtered_html(md_text: str) -> str:
    """Convert Markdown to filtered HTML"""

# utf8_sanitizer.py  
def force_utf8_and_sanitize(content: str, is_html: bool = False) -> str:
    """Sanitize content and ensure UTF-8 encoding"""

# file_processor.py
def process_single_file(input_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
    """Process a single Markdown file"""

def batch_convert_directory(input_dir: Path, output_dir: Path) -> None:
    """Convert all Markdown files in a directory"""
```

---

**Version 2.0** | Modular Architecture | Production Ready | Educational Platform Optimized