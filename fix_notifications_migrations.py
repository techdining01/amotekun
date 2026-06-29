import os

# Delete the auto-generated problematic migrations
migrations_dir = r'c:\Users\USER\Documents\security\amotekun\notifications\migrations'

files_to_delete = [
    '0002_rename_notif_recip_idx_notificatio_recipie_4e3567_idx_and_more.py',
    '0003_rename_notifications_recipient_is_read_idx_notificatio_recipie_4e3567_idx_and_more.py'
]

for filename in files_to_delete:
    filepath = os.path.join(migrations_dir, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Deleted: {filename}")
    else:
        print(f"Not found: {filename}")

print("\nMigration cleanup complete.")
print("Run: python manage.py migrate notifications")
