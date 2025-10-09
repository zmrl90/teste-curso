function setup-venv {
    Write-Host "Setting up Python virtual environment..." -ForegroundColor Cyan
    Write-Host ""
    
    python --version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python is not installed!" -ForegroundColor Red
        return
    }
    
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    
    if (Test-Path ".venv") {
        Remove-Item -Recurse -Force ".venv"
    }
    
    python -m venv .venv
    
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        Write-Host "Virtual environment created!" -ForegroundColor Green
        .\.venv\Scripts\Activate.ps1
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        Write-Host "Setup complete!" -ForegroundColor Green
    } else {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
    }
}