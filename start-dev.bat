@echo off
echo 🚀 Starting Nexora SaaS Development Servers...
echo.

echo 📡 Starting Backend (FastAPI) on http://localhost:8000...
start "Nexora Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo 🎨 Starting Frontend (Next.js) on http://localhost:3000...
start "Nexora Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ✅ Both services are starting!
echo.
echo ════════════════════════════════════════════════
echo 📍 Backend API:  http://localhost:8000
echo 📍 Frontend App: http://localhost:3000
echo 📍 API Docs:     http://localhost:8000/docs
echo ════════════════════════════════════════════════
echo.
echo 💡 Services are running in separate windows.
echo    Close those windows to stop the services.
echo.
pause

