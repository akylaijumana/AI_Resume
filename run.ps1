# AI Resume Generator - Run Script
# Double-click this file or run in PowerShell

Write-Host "==================================="
Write-Host "  AI Resume Generator"
Write-Host "==================================="
Write-Host ""

# Activate virtual environment and run
& .\.venv\Scripts\python.exe app.py

# Pause to see any error messages
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

