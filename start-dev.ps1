# Start both Backend and Frontend for Nexora SaaS
Write-Host "🚀 Starting Nexora SaaS Development Servers..." -ForegroundColor Cyan
Write-Host ""

# Backend
Write-Host "📡 Starting Backend (FastAPI) on http://localhost:8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Frontend
Write-Host "🎨 Starting Frontend (Next.js) on http://localhost:3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

# Wait a bit
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "✅ Both services are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "📍 Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "📍 Frontend App: http://localhost:3000" -ForegroundColor White
Write-Host "📍 API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Services are running in separate windows." -ForegroundColor Cyan
Write-Host "   Close those windows to stop the services." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit this script (services will continue running)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

