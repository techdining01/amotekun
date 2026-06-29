import sys

try:
    with open('app.js', 'rb') as f:
        content = f.read()
        print(f'File size: {len(content)} bytes')
        print(f'Null bytes: {content.count(b"\\x00")}')
        
        # Try to decode and show first 1000 chars
        try:
            text = content.decode('utf-8', errors='ignore')
            print(f'\nFirst 500 characters:\n{text[:500]}')
        except Exception as e:
            print(f'Decode error: {e}')
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
