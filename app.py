"""
AI Resume Generator
Main application entry point
"""
import warnings
import os

# Suppress warnings but allow errors to show
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'


import tkinter as tk
from src.ui.main_window import ResumeGeneratorApp


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ResumeGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

