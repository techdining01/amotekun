@echo off
cd /d "%~dp0"
echo Cleaning up unnecessary files...

REM Remove old corrupted app.js if it exists
if exist "static\js\app.js" (
    echo Backing up old app.js...
    copy "static\js\app.js" "static\js\app.js.backup" >nul 2>&1
    echo Removing old app.js...
    del "static\js\app.js"
)

REM Remove temporary scripts
if exist "cleanup_js.py" del "cleanup_js.py"
if exist "static\js\read_appjs.py" del "static\js\read_appjs.py"

REM Remove redundant batch files (keeping apply_migrations.bat)
if exist "run_migrations.bat" del "run_migrations.bat"

echo Cleanup complete!
pause
