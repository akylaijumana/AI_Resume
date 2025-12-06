# AI Resume Generator Pro

A modern, beautiful AI-powered resume generator with an interactive GUI.

## Features

- 🎨 **Modern UI** - Clean, dark-themed interface with smooth animations
- 🚀 **Fast Generation** - Template mode for instant resume creation
- 🤖 **AI Mode** - Optional AI-enhanced resumes with intelligent content generation
- 💾 **PDF Export** - Save your resume as a professional PDF
- ✨ **Auto-Enhancement** - Automatically adds professional details based on your input

## Installation

### First Time Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Ai_Resume
```

2. Create virtual environment:
```bash
python -m venv .venv
```

3. Activate virtual environment:
```bash
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### On the same device:
```bash
.\.venv\Scripts\Activate.ps1
python resume_generator.py
```

### On a new device (after cloning):
```bash
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python resume_generator.py
```

## Usage

1. **Fill in your information** - Enter name, email, phone, education, skills, and experience
2. **Choose mode** - Template (fast) or AI (enhanced)
3. **Generate** - Click the generate button
4. **Save** - Export as PDF when ready

## Requirements

- Python 3.8+
- reportlab (required)
- transformers & torch (optional, for AI mode)

## License

MIT License

