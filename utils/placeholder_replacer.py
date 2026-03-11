import re

def replace_placeholders(template, profile):
    """Replace {{name}}, {{department}}, {{year}}, {{college}} with profile values."""
    result = template
    for key, value in profile.items():
        if value:
            result = result.replace('{{' + key + '}}', value)
    return result

def get_placeholders(template):
    """Extract all placeholders from a template."""
    return re.findall(r'\{\{(\w+)\}\}', template)
