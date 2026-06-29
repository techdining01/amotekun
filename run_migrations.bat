@echo off
cd /d "%~dp0"
echo Creating migrations for reports app...
python manage.py makemigrations reports
echo.
echo Applying migrations...
python manage.py migrate
echo.
echo Migration complete!
pause
