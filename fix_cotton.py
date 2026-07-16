import os
import re

templates_dir = r'C:\Users\USER\Documents\security\amotekun\templates\dashboard'

for filename in os.listdir(templates_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    in_cotton_tag = False
    changed = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('{% cotton'):
            in_cotton_tag = True
            if '%}' in line and (' / %}' in line or '/%}' in line):
                in_cotton_tag = False
        if in_cotton_tag and '%}' in line:
            if ' / %}' not in line and '/%}' not in line:
                line = line.replace('%}', ' / %}', 1)
                changed = True
            in_cotton_tag = False
        new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed: {filename}')
    else:
        print(f'No changes: {filename}')
