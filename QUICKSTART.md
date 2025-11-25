# Quick Start Guide

## Run on This Device
```powershell
.\.venv\Scripts\python.exe resume_generator.py
```

## Setup on New Device
```powershell
# 1. Delete old venv
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# 2. Create new venv
python -m venv .venv

# 3. Activate
.\.venv\Scripts\Activate.ps1

# 4. Install
pip install -r requirements.txt

# 5. Run
python resume_generator.py
```

## What It Does
- Generates professional resume from basic info
- Adds content you didn't write (skills, responsibilities, summary)
- Two modes: Template (fast) or AI (better)
- Exports to PDF

## Files
- `resume_generator.py` - Main app
- `requirements.txt` - Dependencies
- `README.md` - Full documentation
- `run.ps1` - Easy run script

