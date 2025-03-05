if (-not (Test-Path "pll_venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv pll_venv
} else {
    Write-Host "Virtual environment already exists."
}

.\pll_venv\Scripts\Activate.ps1

if (Test-Path "setup/requirements.txt") {
    Write-Host "Installing requirements from requirements.txt..."
    pip install -r setup/requirements.txt
} else {
    Write-Host "No requirements.txt file found!"
    exit 1
}

    $env:PYTHONPATH = ".\components;$env:PYTHONPATH"

if (Test-Path "setup/setup_test.py") {
    Write-Host "Running the Python script..."
    python setup/setup_test.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "PLLpy has been setup successfully!"
    } else {
        Write-Host "PLLpy has encountered an error while setting up."
        exit 1
    }
} else {
    Write-Host "Python script 'setup/setup_test.py' not found!"
    exit 1
}
