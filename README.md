# AI Resume Generator

A simple, free desktop application that generates professional resumes using AI technology. No API keys required, works completely offline.

## Features

- **100% Free**: No API keys, subscriptions, or hidden costs
- **Offline**: Works without internet connection after initial setup
- **Two Modes**: Template mode (fast) or AI mode (enhanced quality)
- **Smart Generation**: Automatically generates professional summaries, skills, and job responsibilities
- **PDF Export**: Save your resume as a professional PDF document
- **Clean GUI**: Simple and intuitive interface

## Requirements

- Python 3.8 or higher
- Windows OS (PowerShell)

## Installation

### First Time Setup

1. **Open PowerShell** in the project folder

2. **Create virtual environment** (if not exists):
   ```powershell
   python -m venv .venv
   ```

3. **Activate virtual environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
   
   Note: First installation may take 5-10 minutes as it downloads AI models.

## Running the Application

### Method 1: PowerShell
```powershell
.\.venv\Scripts\Activate.ps1
python resume_generator.py
```

### Method 2: Direct Python
```powershell
.\.venv\Scripts\python.exe resume_generator.py
```

## How to Use

1. **Fill in your information**:
   - Name, Email, Phone (required)
   - Education: Your degree, university, year
   - Skills: List your technical and soft skills (comma-separated)
   - Experience: Job title, company, and brief responsibilities

2. **Choose mode**:
   - **Template Mode**: Fast generation with smart formatting
   - **AI Mode**: Enhanced content generation (requires transformers & torch)

3. **Generate**: Click "Generate Resume" button

4. **Review**: Check the generated resume in the output area

5. **Save**: Click "Save as PDF" to export your resume

## Example Input

**Education:**
```
Bachelor of Science in Computer Science
University of California, 2020-2024
```

**Skills:**
```
Python, JavaScript, React, SQL, Problem-solving, Communication
```

**Experience:**
```
Software Developer at Tech Company, 2023-2024
Developed web applications
Collaborated with team
```

**What It Generates:**
- Professional summary based on your background
- Additional relevant skills
- Detailed job responsibilities (even if you only wrote job title)
- Properly formatted sections and structure

## Troubleshooting

### Virtual Environment Issues on New Device

If you copied the project to a new device and get errors:

```powershell
# Remove old virtual environment
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# Create new virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
python resume_generator.py
```

### AI Mode Not Working

If AI mode is unavailable:
- Use Template mode instead (still generates professional content)
- Or install AI libraries: `pip install transformers torch`

### Package Version Errors

If you get torch version errors, edit `requirements.txt` and change:
```
torch>=2.2.0
```
Then reinstall: `pip install -r requirements.txt`

## What Makes This Special

Unlike simple resume templates, this app:
- **Generates content**: Doesn't just format - creates professional summaries and job descriptions
- **Expands input**: Adds relevant skills and details based on what you provide
- **Smart formatting**: Automatically structures your resume professionally
- **Two modes**: Choose between speed (template) or quality (AI)

## Technical Details

- **Language**: Python 3
- **GUI**: Tkinter (built-in)
- **PDF Generation**: ReportLab
- **AI Model**: Google FLAN-T5 (optional, for AI mode)
- **Size**: ~1.5GB with AI model, ~50MB without

## License

Free to use for personal and commercial purposes.

