"""
HTML Filtering Module
Handles HTML tag filtering, sanitization, and structure cleanup.
"""

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


def filter_html(html):
    """Filter HTML content to only include allowed tags and attributes with improved processing."""
    soup = BeautifulSoup(html, 'html.parser')

    # First pass: Handle lists by converting each li to separate p tags
    for ul_tag in soup.find_all(['ul', 'ol']):
        list_items = ul_tag.find_all('li')
        for li in list_items:
            # Create a new paragraph for each list item
            new_p = soup.new_tag('p')
            # Move all contents from li to p
            for content in li.contents[:]:  # Use slice to avoid modification during iteration
                new_p.append(content)
            # Insert the new paragraph after the list
            ul_tag.insert_after(new_p)
        # Remove the original list
        ul_tag.decompose()

    # Second pass: Process all remaining tags
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

    # Third pass: Clean up nested paragraphs and formatting issues
    def clean_nested_paragraphs(element):
        """Recursively clean up nested paragraph tags"""
        if element.name == 'p':
            # Find any nested p tags
            nested_ps = element.find_all('p', recursive=False)
            for nested_p in nested_ps:
                # Move contents of nested p to parent
                for content in nested_p.contents[:]:
                    nested_p.extract()
                    element.append(content)
        
        # Process children
        for child in element.find_all(True, recursive=False):
            clean_nested_paragraphs(child)

    clean_nested_paragraphs(soup)

    # Fourth pass: Fix bold/italic formatting
    for tag in soup.find_all(['em', 'strong']):
        # Check if the content contains markdown-style formatting
        if tag.string:
            text = tag.string
            # Fix **text** inside em tags (should be strong)
            if tag.name == 'em' and text.startswith('**') and text.endswith('**'):
                tag.name = 'strong'
                tag.string = text[2:-2]  # Remove the ** markers
            # Fix *text* inside strong tags (should be em)
            elif tag.name == 'strong' and text.startswith('*') and text.endswith('*') and not text.startswith('**'):
                tag.name = 'em'
                tag.string = text[1:-1]  # Remove the * markers

    # Fifth pass: Clean up empty paragraphs and normalize whitespace
    for p_tag in soup.find_all('p'):
        if not p_tag.get_text().strip():
            p_tag.decompose()
        else:
            # Normalize whitespace but preserve structure
            if p_tag.string:
                p_tag.string = ' '.join(p_tag.string.split())

    # Sixth pass: Handle table formatting issues
    for table in soup.find_all('table'):
        # Ensure proper table structure
        if not table.find('thead') and not table.find('tbody'):
            # If no thead/tbody, assume first row is header
            rows = table.find_all('tr')
            if rows:
                first_row = rows[0]
                # Convert first row cells to th if they aren't already
                for cell in first_row.find_all('td'):
                    cell.name = 'th'
                # Wrap first row in thead
                thead = soup.new_tag('thead')
                thead.append(first_row.extract())
                table.insert(0, thead)
                
                # Wrap remaining rows in tbody if there are any
                remaining_rows = table.find_all('tr')
                if remaining_rows:
                    tbody = soup.new_tag('tbody')
                    for row in remaining_rows:
                        tbody.append(row.extract())
                    table.append(tbody)

    return str(soup)


def md_to_filtered_html(md_text):
    """Convert Markdown text to filtered HTML with improved processing."""
    # Pre-process markdown to handle some edge cases
    md_text = md_text.strip()
    
    # Use comprehensive extensions for better Markdown support
    html = markdown.markdown(
        md_text, 
        extensions=['tables', 'fenced_code', 'codehilite', 'toc', 'attr_list']
    )
    return filter_html(html)
