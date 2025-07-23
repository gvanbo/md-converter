# Markdown to HTML Converter

A powerful tool that converts Markdown files to clean, filtered HTML suitable for websites and Moodle Learning Management Systems. The converter automatically handles encoding issues, sanitizes problematic characters, and ensures output compatibility with educational platforms.

## 🚀 Quick Start

### Installation

1. **Download the converter files** to your project directory
2. **Create input folder**: Make a folder named `md-downloads` 
3. **Add your files**: Place your `.md` files in the `md-downloads` folder
4. **Run the converter**:
   ```bash
   python md-converter.py
   ```
5. **Get results**: Find converted HTML files in `converted-html-descriptions/`

### Requirements

- Python 3.6 or higher
- Internet connection (for automatic package installation)

The converter automatically installs required packages:
- `markdown` - Converts Markdown to HTML
- `beautifulsoup4` - Cleans and filters HTML

## 📁 File Structure

```
your-project/
├── md-converter.py                    # Main application
├── config.py                         # Settings and configuration
├── dependency_manager.py             # Package installer
├── html_filter.py                    # HTML processing
├── utf8_sanitizer.py                 # Character sanitization
├── file_processor.py                 # File operations
├── md-downloads/                     # 📂 Your .md files go here
│   ├── document1.md
│   ├── document2.md
│   └── document3.md
└── converted-html-descriptions/      # 📂 HTML output appears here
    ├── document1.html
    ├── document2.html
    └── document3.html
```

## 🎯 Usage Options

### Option 1: Default Setup (Recommended)
```bash
python md-converter.py
```
- Reads from: `md-downloads/`
- Outputs to: `converted-html-descriptions/`

### Option 2: Custom Directories
```bash
python md-converter.py "path/to/markdown/files" "path/to/output"
```

### Option 3: Get Help
```bash
python md-converter.py --help
```

## ✨ Features

### What Gets Converted

| Markdown Element | HTML Output | Notes |
|-----------------|-------------|--------|
| `# Heading 1` | `<h2>` | H1 converted to H2 for consistency |
| `## Heading 2` | `<h2>` | Primary headings |
| `### Heading 3` | `<h3>` | Secondary headings |
| `**bold text**` | `<strong>` | Bold formatting |
| `*italic text*` | `<em>` | Italic formatting |
| `> Quote` | `<quote>` | Custom quote tags |
| Tables | `<table>` | Full table support |
| `- List items` | `<p>` per item | Lists converted to paragraphs |
| `` `code` `` | `<em>` | Code formatting simplified |

### Character Sanitization

The converter automatically fixes common problems:

- **Smart quotes** → Straight quotes (`"` → `"`)
- **Fancy dashes** → Hyphens (`–` → `-`)
- **Ellipsis** → Three dots (`…` → `...`)
- **Non-breaking spaces** → Regular spaces
- **Encoding artifacts** → Correct characters
- **Asterisks** → Removed (prevents formatting issues)

### HTML Tag Filtering

Only these HTML tags are allowed in the output:
- `<h2>`, `<h3>` - Headings
- `<p>` - Paragraphs  
- `<strong>`, `<em>` - Text emphasis
- `<quote>` - Quotations
- `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>` - Tables

## 🎓 Perfect for Education

### Moodle Compatibility
- Uses only Moodle-approved HTML tags
- Removes problematic formatting that breaks in LMS
- Handles encoding issues that cause display problems
- Optimized for print environments

### Web Integration
- Clean, semantic HTML
- Fast loading pages
- Accessibility-friendly structure
- Easy to style with CSS

## 🔧 Troubleshooting

### Common Issues

**❌ "No Markdown files found"**
- ✅ Check files are in the correct input directory
- ✅ Ensure files have `.md` extension
- ✅ Verify directory path is correct

**❌ "Input directory does not exist"**
- ✅ Create the `md-downloads` folder
- ✅ Check spelling of custom directory paths

**❌ "Permission denied" errors**
- ✅ Ensure write permissions to output directory
- ✅ Try running as administrator (Windows) or with sudo (Mac/Linux)

**❌ Files look corrupted or have weird characters**
- ✅ The converter handles this automatically
- ✅ Check your original files aren't already corrupted
- ✅ Try with a simple test file first

### Getting Detailed Feedback

The converter provides helpful progress information:

```
Checking system requirements...
✓ Python 3.8 detected

Checking required packages...
✓ markdown is already installed
✓ beautifulsoup4 is already installed

Configuration:
  Input directory:  md-downloads
  Output directory: converted-html-descriptions

Found 3 Markdown files to convert...
Converting: intro.md -> intro.html
  ✓ Successfully converted
Converting: guide.md -> guide.html
  Note: Read guide.md using cp1252 encoding
  ✓ Successfully converted

Conversion complete!
Successfully converted: 2 files
Failed to convert: 0 files

Applying UTF-8 encoding and sanitization...
Processed and sanitized: 2 files

HTML files saved in: converted-html-descriptions
```

## 📝 Best Practices

### File Preparation
1. **Use descriptive filenames** - HTML files will have the same names
2. **Test with small batches** first to verify output quality
3. **Keep backups** of your original Markdown files
4. **Use standard Markdown syntax** for best results

### Quality Assurance
1. **Review converted files** before uploading to your platform
2. **Test in target environment** (your website or Moodle)
3. **Check for formatting issues** in both web and print views

### Workflow Tips
1. **Organize by project** - use separate directories for different courses/projects
2. **Batch similar content** - process related files together
3. **Version control** - keep track of changes to your source files

## 🆘 Getting Help

If you encounter issues:

1. **Check this README** for common solutions
2. **Review the error messages** - they're designed to be helpful
3. **Try with a simple test file** to isolate the problem
4. **Check file encodings** if you see strange characters
5. **Visit the project documentation** for advanced usage

## 📊 Technical Specifications

- **Input formats**: `.md`, `.markdown`, `.txt`
- **Output format**: `.html` (UTF-8 encoded)
- **Supported encodings**: UTF-8, CP1252, Latin-1, ISO-8859-1
- **Processing speed**: ~50-100 files per second (depending on file size)
- **Memory usage**: Minimal (processes files one at a time)

---

**Version 2.0** | Built for educators and content creators | Optimized for Moodle and web platforms
