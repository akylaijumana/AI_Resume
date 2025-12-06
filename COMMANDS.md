# Quick Commands Reference

## After Cloning on New Device

Run these commands in PowerShell **in order**:

```powershell
# 1. Navigate to project
cd C:\Users\YourUsername\PycharmProjects\AI_RESUME

# 2. Remove old virtual environment (if exists)
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# 3. Create new virtual environment
python -m venv .venv

# 4. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the application
python resume_generator.py
```

## Daily Use (After Initial Setup)

```powershell
# Activate and run
.\.venv\Scripts\Activate.ps1
python resume_generator.py
```

## One-Line Command (Daily Use)

```powershell
.\.venv\Scripts\Activate.ps1; python resume_generator.py
```

## Fix Execution Policy Error

If you get "cannot be loaded because running scripts is disabled":

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

