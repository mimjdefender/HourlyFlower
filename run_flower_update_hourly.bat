@echo off
echo.
echo 🌿 Starting Flower Graphic Update...
echo ================================================

:: Run the flower slide component
python flower_slide_component.py

echo.
echo ✅ Update complete! Next update in 1 hour.
timeout /t 3600 /nobreak
goto :eof 