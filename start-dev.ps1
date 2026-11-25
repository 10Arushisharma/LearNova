#!/usr/bin/env pwsh
# Learnova dev startup script — Windows PowerShell
# Usage: ./start-dev.ps1

Write-Host "🚀 Starting Learnova Development Environment" -ForegroundColor Cyan

# Start backend in a new window
Write-Host "▶ Starting backend on http://localhost:8000" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot\backend'; .\.venv\Scripts\uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000"

# Wait a moment for backend to boot
Start-Sleep -Seconds 3

# Start frontend in a new window
Write-Host "▶ Starting frontend on http://localhost:5173" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot\frontend'; cmd /c 'npm run dev'"

Write-Host ""
Write-Host "✅ Learnova is starting!" -ForegroundColor Green
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000/api/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop." -ForegroundColor Gray
