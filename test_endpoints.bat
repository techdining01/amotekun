@echo off
cd /d "%~dp0"
echo Testing Endpoints for assurance...
echo.
# Test incidents endpoint
curl http://localhost:8000/api/incidents/

# Test police stations
curl http://localhost:8000/api/stations/police/

# Test Amotekun stations
curl http://localhost:8000/api/stations/amotekun/