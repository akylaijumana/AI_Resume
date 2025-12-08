"""
Main Application UI
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading

from src.config import COLORS, WINDOW_CONFIG
from src.ui.widgets import ModernButton
from src.engine import ResumeEngine, AI_AVAILABLE
from src.pdf_exporter import PDFExporter


class ResumeGeneratorApp:
    """Main application class"""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_CONFIG['title'])
        self.root.geometry(f"{WINDOW_CONFIG['width']}x{WINDOW_CONFIG['height']}")
        self.root.configure(bg=COLORS['bg_gradient_start'])

        self.engine = ResumeEngine()
        self.setup_ui()

    def setup_ui(self):
        """Setup main user interface"""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Main canvas for scrolling
        canvas = tk.Canvas(self.root, bg=COLORS['bg_gradient_start'], highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.root, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=canvas.yview)

        main_frame = tk.Frame(canvas, bg=COLORS['bg_gradient_start'])
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor="nw")

        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)

        main_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Header
        self.create_header(main_frame)

        # Mode selection
        self.create_mode_selection(main_frame)

        # Status
        self.status_label = tk.Label(
            main_frame,
            text="● Ready to generate",
            font=("Segoe UI", 10),
            fg=COLORS['success'],
            bg=COLORS['bg_gradient_start']
        )
        self.status_label.pack(pady=(0, 15))

        # Input fields
        self.create_input_section(main_frame)

        # Generate button
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_gradient_start'])
        button_frame.pack(pady=25)

        self.generate_btn = ModernButton(
            button_frame,
            "✨ Generate Resume",
            self.generate_resume,
            bg_color=COLORS['accent_color'],
            hover_color=COLORS['accent_hover'],
            width=250,
            height=55
        )
        self.generate_btn.pack()

        # Output section
        self.create_output_section(main_frame)

        # Save button
        save_button_frame = tk.Frame(main_frame, bg=COLORS['bg_gradient_start'])
        save_button_frame.pack(pady=(10, 40))

        self.save_btn = ModernButton(
            save_button_frame,
            "💾 Save as PDF",
            self.save_to_pdf,
            bg_color="#10B981",
            hover_color="#059669",
            width=200,
            height=50
        )
        self.save_btn.pack()

    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=COLORS['bg_gradient_start'], height=120)
        header_frame.pack(fill="x", padx=40, pady=(30, 20))

        title_label = tk.Label(
            header_frame,
            text="✨ AI Resume Generator Pro",
            font=("Segoe UI", 32, "bold"),
            fg=COLORS['text_color'],
            bg=COLORS['bg_gradient_start']
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Create professional resumes powered by AI in seconds",
            font=("Segoe UI", 12),
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_gradient_start']
        )
        subtitle_label.pack(pady=(5, 0))

    def create_mode_selection(self, parent):
        """Create mode selection card"""
        mode_card = tk.Frame(parent, bg=COLORS['card_bg'], bd=0)
        mode_card.pack(fill="x", padx=40, pady=(0, 20))

        mode_inner = tk.Frame(mode_card, bg=COLORS['card_bg'])
        mode_inner.pack(padx=25, pady=20)

        mode_title = tk.Label(
            mode_inner,
            text="⚡ Generation Mode",
            font=("Segoe UI", 13, "bold"),
            fg=COLORS['text_color'],
            bg=COLORS['card_bg']
        )
        mode_title.pack(anchor="w", pady=(0, 10))

        self.mode_var = tk.StringVar(value="template")

        mode_options = tk.Frame(mode_inner, bg=COLORS['card_bg'])
        mode_options.pack(fill="x")

        template_rb = tk.Radiobutton(
            mode_options,
            text="🚀 Template Mode (Fast)",
            variable=self.mode_var,
            value="template",
            font=("Segoe UI", 11),
            fg=COLORS['text_color'],
            bg=COLORS['card_bg'],
            selectcolor=COLORS['accent_color'],
            activebackground=COLORS['card_bg'],
            activeforeground=COLORS['text_color']
        )
        template_rb.pack(side="left", padx=10)

        if AI_AVAILABLE:
            ai_rb = tk.Radiobutton(
                mode_options,
                text="🤖 AI Mode (Premium Quality)",
                variable=self.mode_var,
                value="ai",
                font=("Segoe UI", 11),
                fg=COLORS['text_color'],
                bg=COLORS['card_bg'],
                selectcolor=COLORS['accent_color'],
                activebackground=COLORS['card_bg'],
                activeforeground=COLORS['text_color']
            )
            ai_rb.pack(side="left", padx=10)
        else:
            info_label = tk.Label(
                mode_options,
                text="(AI mode: Install transformers & torch)",
                font=("Segoe UI", 9),
                fg="#64748B",
                bg=COLORS['card_bg']
            )
            info_label.pack(side="left", padx=10)

    def create_input_section(self, parent):
        """Create input fields section"""
        input_card = tk.Frame(parent, bg=COLORS['card_bg'])
        input_card.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        input_inner = tk.Frame(input_card, bg=COLORS['card_bg'])
        input_inner.pack(padx=30, pady=25, fill="both", expand=True)

        card_title = tk.Label(
            input_inner,
            text="📝 Your Information",
            font=("Segoe UI", 15, "bold"),
            fg=COLORS['text_color'],
            bg=COLORS['card_bg']
        )
        card_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        # Input fields
        row = 1
        self.create_input_field(input_inner, row, "👤 Full Name", is_entry=True, var_name="name_entry")
        row += 1

        self.create_input_field(input_inner, row, "📧 Email", is_entry=True, var_name="email_entry")
        row += 1

        self.create_input_field(input_inner, row, "📱 Phone", is_entry=True, var_name="phone_entry")
        row += 1

        self.create_input_field(input_inner, row, "🎓 Education", height=4, var_name="education_text")
        row += 1

        self.create_input_field(input_inner, row, "💼 Skills", height=4, var_name="skills_text")
        row += 1

        self.create_input_field(input_inner, row, "🏢 Experience", height=5, var_name="experience_text")

        input_inner.columnconfigure(1, weight=1)

    def create_input_field(self, parent, row, label_text, is_entry=False, height=1, var_name=None):
        """Create a modern input field"""
        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 11, "bold"),
            fg=COLORS['text_color'],
            bg=COLORS['card_bg']
        )
        label.grid(row=row, column=0, sticky="nw", pady=(8, 0), padx=(0, 20))

        if is_entry:
            entry = tk.Entry(
                parent,
                font=("Segoe UI", 11),
                bg="#0F172A",
                fg="#E2E8F0",
                insertbackground="white",
                relief="flat",
                bd=0
            )
            entry.grid(row=row, column=1, sticky="ew", pady=8, ipady=8, ipadx=10)
            setattr(self, var_name, entry)
        else:
            text_widget = scrolledtext.ScrolledText(
                parent,
                font=("Segoe UI", 10),
                bg="#0F172A",
                fg="#E2E8F0",
                insertbackground="white",
                relief="flat",
                bd=0,
                height=height,
                wrap=tk.WORD,
                padx=10,
                pady=8
            )
            text_widget.grid(row=row, column=1, sticky="ew", pady=8)
            setattr(self, var_name, text_widget)

    def create_output_section(self, parent):
        """Create output display section"""
        output_card = tk.Frame(parent, bg=COLORS['card_bg'])
        output_card.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        output_inner = tk.Frame(output_card, bg=COLORS['card_bg'])
        output_inner.pack(padx=30, pady=25, fill="both", expand=True)

        output_title = tk.Label(
            output_inner,
            text="📄 Generated Resume",
            font=("Segoe UI", 15, "bold"),
            fg=COLORS['text_color'],
            bg=COLORS['card_bg']
        )
        output_title.pack(anchor="w", pady=(0, 15))

        self.output_text = scrolledtext.ScrolledText(
            output_inner,
            font=("Consolas", 10),
            bg="#0F172A",
            fg="#E2E8F0",
            insertbackground="white",
            relief="flat",
            padx=15,
            pady=15,
            wrap=tk.WORD
        )
        self.output_text.pack(fill="both", expand=True)

    def generate_resume(self):
        """Generate resume based on user input"""
        # Get input data
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        education = self.education_text.get("1.0", tk.END).strip()
        skills = self.skills_text.get("1.0", tk.END).strip()
        experience = self.experience_text.get("1.0", tk.END).strip()

        # Validate
        if not name:
            messagebox.showwarning("⚠️ Missing Information", "Please enter your name.")
            return

        # Update status
        self.status_label.config(text="⏳ Generating resume...", fg="#F59E0B")
        self.generate_btn.config(state='disabled')

        data = {
            'name': name,
            'email': email,
            'phone': phone,
            'education': education,
            'skills': skills,
            'experience': experience,
        }

        mode = self.mode_var.get()

        def generate_thread():
            try:
                resume_text = self.engine.generate_resume(data, mode)

                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", resume_text)

                self.status_label.config(text="✅ Resume generated successfully!", fg=COLORS['success'])
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to generate resume: {str(e)}")
                self.status_label.config(text="❌ Generation failed", fg=COLORS['error'])
            finally:
                self.generate_btn.config(state='normal')

        thread = threading.Thread(target=generate_thread, daemon=True)
        thread.start()

    def save_to_pdf(self):
        """Save resume to PDF file"""
        resume_text = self.output_text.get("1.0", tk.END).strip()

        if not resume_text:
            messagebox.showwarning("⚠️ No Resume", "No resume to save. Generate a resume first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="resume.pdf"
        )

        if not file_path:
            return

        try:
            PDFExporter.export(resume_text, file_path)
            messagebox.showinfo("✅ Success", f"Resume saved successfully!\n\n{file_path}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to save PDF: {str(e)}")

