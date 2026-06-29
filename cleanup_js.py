import os
import shutil

js_dir = r'c:\Users\USER\Documents\security\amotekun\static\js'
old_app = os.path.join(js_dir, 'app.js')
backup_app = os.path.join(js_dir, 'app.js.backup')
read_script = os.path.join(js_dir, 'read_appjs.py')

# Try to backup old app.js if it exists
if os.path.exists(old_app):
    try:
        shutil.copy2(old_app, backup_app)
        print(f"Backed up app.js to app.js.backup")
        os.remove(old_app)
        print(f"Removed old app.js")
    except Exception as e:
        print(f"Could not backup/remove app.js: {e}")

# Remove read script if it exists
if os.path.exists(read_script):
    try:
        os.remove(read_script)
        print(f"Removed read_appjs.py")
    except Exception as e:
        print(f"Could not remove read_appjs.py: {e}")

print("Cleanup complete")
