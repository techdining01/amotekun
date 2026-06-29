@echo off
cd /d "%~dp0"
echo Applying migrations...
python manage.py migrate
echo.
echo Migration complete!
pause
