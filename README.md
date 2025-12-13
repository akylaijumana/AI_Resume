# AI Resume Generator Pro

A desktop application for generating professional resumes with AI assistance. Features a modern girly-themed interface with pink and purple colors.

---

## ✨ Features

- **Two Generation Modes**
  - Template Mode: Instant generation using smart templates
  - AI Mode: Creative generation using Google FLAN-T5 model

- **Save & Load System**
  - Save your input data for reuse
  - Save generated resumes to collection
  - SQLite database for local storage

- **PDF Export**
  - Export any generated resume to PDF
  - Professional formatting
  - Ready to send to employers

- **Modern UI**
  - Girly color scheme (pink, purple, lavender, mint)
  - Compact 950x750 window
  - Clean and intuitive interface

- **100% Local & Private**
  - No internet connection required
  - All data stays on your computer
  - No tracking or telemetry

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Ai_Resume
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows:**
```powershell
.\.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```

---

## 📦 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended for AI mode)
- **Storage**: ~500MB for dependencies + AI model

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| GUI | Tkinter (built-in) |
| AI Model | Google FLAN-T5-Base (220M params) |
| ML Framework | Transformers 4.44.0 + PyTorch 2.2+ |
| Database | SQLite3 (built-in) |
| PDF Export | ReportLab 4.0.7 |

---

## 🧩 Architecture Overview

This is a single desktop application (no separate client/server and no external API). Modules interact locally:

```
+-------------------+
|     app.py        |  Entry point; wires UI and engine
+---------+---------+
          |
          v
+-------------------+        +-------------------+
|   UI (Tkinter)    | -----> |  pdf_exporter.py  |  Export to PDF
| src/ui/*.py       |        +-------------------+
+---------+---------+
          |
          v
+-------------------+        +-------------------+
|   engine.py       | <----> |   database.py     |  SQLite CRUD
| generation logic  |        +-------------------+
+-------------------+
```

---

## 📖 How to Use

### Generate a Resume

1. Fill in your information:
   - Full Name
   - Email & Phone
   - Education
   - Skills
   - Work Experience

2. Choose generation mode:
   - **Template Mode**: Fast (< 1 second)
   - **AI Mode**: Creative (5-15 seconds)

3. Click **"Generate Resume"**

4. Review the generated resume in the output area

5. Export to PDF or save to database

### Save Input Data

1. Fill in your information
2. Click **"Save Current"** in the "My Saved Resumes" section
3. Your data is saved to database
4. Select from dropdown and click **"Load Resume"** to reload

### Save Generated Resume

1. After generating a resume
2. Click **"Save Generated"** in the "Manage Generated Resume" section
3. Enter a title (e.g., "Software Engineer Resume")
4. Select from dropdown and click **"Load"** to view later

---

## 💾 Database

The app uses SQLite for local storage:

- **Location**: `resumes.db` in project root
- **Auto-created**: No setup required
- **Two tables**:
  - `resumes` - Stores input data
  - `generated_resumes` - Stores generated outputs

**Backup**: Just copy the `resumes.db` file

---

## 🤖 AI Generation

### Template Mode
- Uses predefined phrases and templates
- Smart categorization by job type
- Random selection for variety
- Instant results

### AI Mode
- Uses Google FLAN-T5-Base model
- Generates unique, creative text
- First use: Downloads model (~500MB)
- Subsequent uses: Loads from cache

---

## 🔌 API Requests

- There are no external API endpoints. All processing is done locally within the application.

---

## ⚡ Performance

| Action | Time |
|--------|------|
| App Startup | < 2 seconds |
| Template Generation | < 1 second |
| AI Model Loading | 10-15 seconds (first time only) |
| AI Generation | 5-15 seconds |
| PDF Export | < 1 second |
| Database Save/Load | < 0.1 seconds |

---

## 🔧 Troubleshooting

### AI Mode Not Working
```bash
# Install AI dependencies
pip install transformers torch
```

### Database Errors
```bash
# Delete the database file (Windows PowerShell)
Remove-Item .\resumes.db
# Restart the app - it will recreate automatically
```

### PDF Export Fails
```bash
# Reinstall ReportLab
pip install --force-reinstall reportlab
```

### App Won't Start
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📁 Project Structure

```
Ai_Resume/
├── app.py                    # Entry point
├── requirements.txt          # Dependencies
├── resumes.db                # Database (auto-created)
├── src/
│   ├── config.py             # Colors and settings
│   ├── engine.py             # Resume generation logic
│   ├── pdf_exporter.py       # PDF creation
│   ├── database.py           # SQLite operations
│   └── ui/
│       ├── main_window.py    # Main interface
│       └── widgets.py        # Custom buttons
└── doc/                      # Documentation
```

---

## 🧭 Commit History (optional)

- Use meaningful commit messages (e.g., feat: add AI mode, fix: handle empty skills)
- Keep clean branching: `main` for stable, feature branches for work in progress
- Prefer small, atomic commits

---

## 🎯 Key Benefits

✅ **Fast Setup** - Just install and run  
✅ **No Account Needed** - Fully offline  
✅ **Privacy Protected** - Data stays local  
✅ **Easy to Use** - Intuitive interface  
✅ **Professional Output** - ATS-friendly PDFs  
✅ **Unlimited Saves** - Store as many resumes as you want  
✅ **AI Powered** - Optional creative generation  
✅ **Cross-Platform** - Works on Windows, Mac, Linux  

---

## 📝 Example Output

```
JOHN DOE
john@email.com | +1-234-567-8900
================================================================================

PROFESSIONAL SUMMARY
--------------------------------------------------------------------------------
Results-driven professional with expertise in Python, JavaScript, React...

CORE COMPETENCIES
--------------------------------------------------------------------------------
Technical Skills: Python, JavaScript, React, SQL, Git
Professional Skills: Leadership, Communication, Problem-solving

PROFESSIONAL EXPERIENCE
--------------------------------------------------------------------------------

SOFTWARE ENGINEER
Tech Company | 2020-2023
  • Developed and maintained applications using modern technologies
  • Collaborated with cross-functional teams to deliver projects
  • Optimized performance and improved efficiency by 30%
  • Participated in code reviews and maintained quality standards

EDUCATION
--------------------------------------------------------------------------------
• Bachelor of Science in Computer Science, University Name, 2020
```

---

## 🌐 Language Support

- **Interface**: English
- **Generated Resumes**: English (can be edited manually)

---

## 💬 Support

Having issues? Check:
1. Python version (3.8+)
2. All dependencies installed
3. Virtual environment activated
4. Enough disk space (~1GB)

For detailed technical info, see files in the `doc/` folder.
