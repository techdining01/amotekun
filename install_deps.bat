@echo off
cd /d "%~dp0"
echo Installing django-allauth and updating dependencies...
python -m pip install -e .
echo.
echo Installation complete!
pause
