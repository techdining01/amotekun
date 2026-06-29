@echo off
cd /d "%~dp0"
echo Setting up Real-Time Alerts with Django Channels...
echo.

echo Step 1: Removing conflicting migration...
if exist "dispatch\migrations\0002_dispatch_timestamps.py" (
    del "dispatch\migrations\0002_dispatch_timestamps.py"
    echo Removed conflicting migration file.
)
echo.

echo Step 2: Installing dependencies...
python -m pip install -e .
echo.

echo Step 3: Creating migrations for notifications...
python manage.py makemigrations notifications
echo.

echo Step 4: Applying migrations...
python manage.py migrate
echo.

echo Real-Time Alerts setup complete!
echo.
echo IMPORTANT: Redis must be running for WebSocket notifications to work.
echo.
echo To start Redis (if installed):
echo   redis-server
echo.
echo To start the server with Daphne (ASGI):
echo   daphne -b 0.0.0.0 -p 8000 incident.asgi:application
echo.
echo Or use runserver for development (WebSockets may be limited):
echo   python manage.py runserver
pause
