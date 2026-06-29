@echo off
cd /d "%~dp0"
echo Setting up Phase 9: Frontend Integration...
echo.

echo Step 1: Creating migrations for chat...
python manage.py makemigrations chat
echo.

echo Step 2: Creating migrations for surveillance...
python manage.py makemigrations surveillance
echo.

echo Step 3: Applying migrations...
python manage.py migrate
echo.

echo Phase 9 setup complete!
echo.
echo New Features:
echo - Sound alerts (chat, critical, severity)
echo - Real-time chat for operatives
echo - CCTV camera integration with MAC address/camera ID
echo.
echo Next steps:
echo 1. Add actual audio files to static/audio/
echo 2. Test chat endpoints
echo 3. Add cameras via admin panel
echo 4. Integrate WebSocket client in dashboards
pause
