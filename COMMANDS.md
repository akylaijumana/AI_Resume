# Development Commands

## Project Structure
```
Ai_Resume/
├── app.py                  # Main entry point
├── src/                    # Source code
│   ├── config.py          # Configuration
│   ├── engine.py          # Resume generation
│   ├── pdf_exporter.py    # PDF export
│   └── ui/                # User interface
│       ├── main_window.py # Main UI
│       └── widgets.py     # Custom widgets
└── requirements.txt        # Dependencies
```

## Quick Start

### Run Application
```powershell
# Using run script (recommended)
.\run.ps1

# Manual
.\.venv\Scripts\Activate.ps1
python app.py
```

## Development Commands

### Setup New Environment
```powershell
# Automated setup
.\setup_new_device.ps1

# Manual setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### Activate Virtual Environment
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate
```

### Package Management
```powershell
# Install dependencies
pip install -r requirements.txt

# Add new package
pip install <package-name>
pip freeze > requirements.txt

# Update all packages
pip list --outdated
pip install --upgrade <package-name>
```

### Running Components

#### Run Main Application
```powershell
python app.py
```

#### Test Individual Modules
```powershell
# Test engine
python -c "from src.engine import ResumeEngine; e = ResumeEngine(); print('Engine OK')"

# Test config
python -c "from src.config import COLORS; print('Config OK')"
```

## Code Quality

### Style Checking
```powershell
# Install tools
pip install flake8 autopep8

# Check style
flake8 src/ app.py

# Auto-format
autopep8 --in-place --recursive src/ app.py
```

### Type Checking
```powershell
# Install mypy
pip install mypy

# Run type check
mypy src/ app.py
```

## Troubleshooting

### Reset Virtual Environment
```powershell
Remove-Item -Recurse -Force .venv
.\setup_new_device.ps1
```

### Clear Python Cache
```powershell
Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse -Force | Remove-Item -Recurse -Force
```

### Check Python Version
```powershell
python --version
```

### Verify Installation
```powershell
.\.venv\Scripts\Activate.ps1
pip list
```

## Git Commands

### Initial Setup
```powershell
git init
git add .
git commit -m "Initial commit"
```

### Daily Workflow
```powershell
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push to remote
git push origin main
```

### Useful Git Commands
```powershell
# View history
git log --oneline

# Create branch
git checkout -b feature-name

# Merge branch
git checkout main
git merge feature-name

# Pull latest
git pull origin main
```

