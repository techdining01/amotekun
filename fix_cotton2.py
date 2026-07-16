import os

files_to_fix = [
    r'C:\Users\USER\Documents\security\amotekun\templates\dashboard\super_admin_dashboard.html',
    r'C:\Users\USER\Documents\security\amotekun\templates\dashboard\officer_dashboard.html',
]

for filepath in files_to_fix:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix self-closing statistics_card followed by {% endcotton %}
    # Pattern: {% cotton statistics_card ... / %}{% endcotton %}
    # Remove the {% endcotton %}
    content = content.replace('/ %}{% endcotton %}', '/ %}')
    
    # Fix self-closing card tags that have content after them
    # Pattern: {% cotton card  / %}\n        {% cotton:slot header  / %}
    # Should be: {% cotton card %}\n        {% cotton:slot header %}
    content = content.replace('{% cotton card  / %}', '{% cotton card %}')
    content = content.replace('{% cotton:slot header  / %}', '{% cotton:slot header %}')
    content = content.replace('{% cotton:slot body  / %}', '{% cotton:slot body %}')
    content = content.replace('{% cotton:slot footer  / %}', '{% cotton:slot footer %}')
    
    # Fix button self-closing tags that have content after them
    content = content.replace('{% cotton button variant="primary"  / %}', '{% cotton button variant="primary" %}')
    content = content.replace('{% cotton button variant="secondary"  / %}', '{% cotton button variant="secondary" %}')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {filepath}')
    else:
        print(f'No changes: {filepath}')
