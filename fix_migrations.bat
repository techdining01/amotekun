@echo off
cd /d "%~dp0"
echo Fixing notifications migrations...
python fix_notifications_migrations.py
echo.
echo Applying migrations...
python manage.py migrate notifications
pause
