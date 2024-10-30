import markdown
import bleach
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdownify')
def markdownify(text, line_count=0):
    """
    Converts Markdown text to HTML and truncates to a specified number of lines.

    Parameters:
    - text (str): The input Markdown text.
    - line_count (int): The number of lines to display. If 0, display all lines.

    Returns:
    - Safe HTML string of processed Markdown content.
    """

    # Split the text into lines
    lines = text.splitlines()

    # Truncate the text to the specified number of lines
    if line_count > 0:
        truncated_text = "\n".join(lines[:line_count])
    else:
        truncated_text = text  # Use the full text if no line limit is specified

    # Specify Markdown extensions to use
    extensions = [
        'extra',
        'admonition',
        'codehilite',
        'legacy_attrs',
        'legacy_em',
        'meta',
        'nl2br',
        'sane_lists',
        'smarty',
        'toc'
    ]

    # Convert Markdown to HTML using specified extensions
    html = markdown.markdown(truncated_text, extensions=extensions, output_format='html')

    # Define allowed HTML tags and attributes for security
    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
        'li', 'ol', 'strong', 'ul', 'p', 'h1', 'h2', 'h3', 'pre', 'br'
    ]
    allowed_attributes = {
        'a': ['href', 'title'],
        'abbr': ['title'],
        'acronym': ['title']
    }

    # Clean the HTML to remove any disallowed tags/attributes
    clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)

    # Mark the resulting HTML as safe to prevent escaping in Django templates
    return mark_safe(clean_html)
