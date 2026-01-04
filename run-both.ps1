# Simple script to run both backend and frontend
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $scriptPath "backend"
$frontendDir = Join-Path $scriptPath "frontend"

Write-Host "🚀 Starting Nexora SaaS..." -ForegroundColor Cyan
Write-Host ""

# Start Backend
Write-Host "📡 Starting Backend on http://localhost:8000..." -ForegroundColor Yellow
$backendCmd = "cd /d `"$backendDir`" && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
Start-Process cmd -ArgumentList "/k", $backendCmd

Start-Sleep -Seconds 3

# Start Frontend  
Write-Host "🎨 Starting Frontend on http://localhost:3000..." -ForegroundColor Yellow
$frontendCmd = "cd /d `"$frontendDir`" && npm run dev"
Start-Process cmd -ArgumentList "/k", $frontendCmd

Write-Host ""
Write-Host "✅ Both services are starting in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "📍 Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "📍 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "💡 Close the command windows to stop the services." -ForegroundColor Cyan
Write-Host ""

