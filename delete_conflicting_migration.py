import os

# Delete the conflicting migration file
migration_file = r'c:\Users\USER\Documents\security\amotekun\dispatch\migrations\0002_dispatch_timestamps.py'

if os.path.exists(migration_file):
    os.remove(migration_file)
    print(f"Deleted conflicting migration: {migration_file}")
else:
    print(f"File not found: {migration_file}")
