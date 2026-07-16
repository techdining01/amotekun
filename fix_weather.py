import os, glob

W = '<div hx-get="{% url \'weather-widget\' %}" hx-trigger="load" hx-swap="outerHTML"><div class="animate-pulse h-32 rounded-xl bg-slate-100"></div></div>'
T = '<div hx-get="{% url \'traffic-widget\' %}" hx-trigger="load" hx-swap="outerHTML"><div class="animate-pulse h-32 rounded-xl bg-slate-100"></div></div>'

KEYS = {
    'dashboard/widgets/weather.html': W,
    'dashboard/widgets/traffic.html': T,
    'cotton/weather/weather_widget.html': W,
    'cotton/traffic/traffic_widget.html': T,
}

for path in glob.glob('templates/dashboard/*.html'):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    new_lines = []
    changed = False
    for line in lines:
        matched = False
        for key, repl in KEYS.items():
            if key in line and 'include' in line:
                indent = ' ' * (len(line) - len(line.lstrip()))
                new_lines.append(indent + repl + '\n')
                matched = True
                changed = True
                break
        if not matched:
            new_lines.append(line)
    if changed:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.writelines(new_lines)
        print('Updated:', os.path.basename(path))

print('done')
