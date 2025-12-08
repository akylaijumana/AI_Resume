"""
AI Resume Generator
Main application entry point
"""
import tkinter as tk
from src.ui.main_window import ResumeGeneratorApp


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ResumeGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

