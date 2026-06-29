@echo off
cd /d "%~dp0"
echo Setting up django-allauth authentication...
echo.

echo Step 1: Installing dependencies...
python -m pip install -e .
echo.

echo Step 2: Creating migrations...
python manage.py makemigrations
echo.

echo Step 3: Applying migrations...
python manage.py migrate
echo.

echo Step 4: Creating superuser (optional)...
echo Run: python manage.py createsuperuser
echo.

echo Authentication setup complete!
echo.
echo Next steps:
echo 1. Run: python manage.py createsuperuser (to create admin account)
echo 2. Start server: python manage.py runserver
echo 3. Visit: http://localhost:8000/accounts/login/
pause
