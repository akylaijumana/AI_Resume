"""
Main Application UI
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import threading

from src.config import COLORS, WINDOW_CONFIG
from src.ui.widgets import ModernButton
from src.engine import ResumeEngine, AI_AVAILABLE
from src.pdf_exporter import PDFExporter
from src.database import ResumeDatabase


class ResumeGeneratorApp:
    """Main application class"""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_CONFIG['title'])
        self.root.geometry(f"{WINDOW_CONFIG['width']}x{WINDOW_CONFIG['height']}")
        self.root.configure(bg=COLORS['bg_gradient_start'])

        self.engine = ResumeEngine()
        self.db = ResumeDatabase()
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

        # Save/Load section
        self.create_save_load_section(main_frame)

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
            "Generate Resume",
            self.generate_resume,
            bg_color=COLORS['accent_color'],
            hover_color=COLORS['accent_hover'],
            width=220,
            height=50
        )
        self.generate_btn.pack()

        # Output section
        self.create_output_section(main_frame)

        # Save/Load Generated Resume Section
        self.create_generated_resume_controls(main_frame)

    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=COLORS['bg_gradient_start'], height=120)
        header_frame.pack(fill="x", padx=40, pady=(30, 20))

        title_label = tk.Label(
            header_frame,
            text="AI Resume Generator Pro",
            font=("Segoe UI", 28, "bold"),
            fg=COLORS['pink'],
            bg=COLORS['bg_gradient_start']
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Create professional resumes powered by AI",
            font=("Segoe UI", 11),
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
            text="Generation Mode",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS['lavender'],
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

    def create_save_load_section(self, parent):
        """Create save/load section with girly aesthetic"""
        save_load_card = tk.Frame(parent, bg=COLORS['card_bg'], bd=0)
        save_load_card.pack(fill="x", padx=40, pady=(0, 20))

        save_load_inner = tk.Frame(save_load_card, bg=COLORS['card_bg'])
        save_load_inner.pack(padx=30, pady=20)

        # Title
        section_title = tk.Label(
            save_load_inner,
            text="My Saved Resumes",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS['pink'],
            bg=COLORS['card_bg']
        )
        section_title.pack(anchor="w", pady=(0, 12))

        # Button row
        button_row = tk.Frame(save_load_inner, bg=COLORS['card_bg'])
        button_row.pack(fill="x", pady=(0, 12))

        # Save button
        save_btn = ModernButton(
            button_row,
            "Save Current",
            self.save_current_resume,
            bg_color=COLORS['accent_color'],
            hover_color=COLORS['accent_hover'],
            width=140,
            height=38
        )
        save_btn.pack(side="left", padx=(0, 10))

        # Load button
        load_btn = ModernButton(
            button_row,
            "Load Resume",
            self.load_selected_resume,
            bg_color=COLORS['lavender'],
            hover_color="#8B5CF6",
            width=130,
            height=38
        )
        load_btn.pack(side="left", padx=(0, 10))

        # Refresh button
        refresh_btn = ModernButton(
            button_row,
            "Refresh",
            self.refresh_resume_list,
            bg_color=COLORS['mint'],
            hover_color="#34D399",
            width=100,
            height=38
        )
        refresh_btn.pack(side="left")

        # Dropdown section
        dropdown_frame = tk.Frame(save_load_inner, bg=COLORS['card_bg'])
        dropdown_frame.pack(fill="x")

        dropdown_label = tk.Label(
            dropdown_frame,
            text="Select a saved resume:",
            font=("Segoe UI", 10),
            fg=COLORS['coral'],
            bg=COLORS['card_bg']
        )
        dropdown_label.pack(side="left", padx=(0, 12))

        self.resume_var = tk.StringVar()

        # Style the combobox
        style = ttk.Style()
        style.configure('Pink.TCombobox',
                       fieldbackground='#1E293B',
                       background='#E879F9',
                       foreground='white')

        self.resume_dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.resume_var,
            state="readonly",
            width=45,
            font=("Segoe UI", 10),
            style='Pink.TCombobox'
        )
        self.resume_dropdown.pack(side="left")

        # load saved resumes
        self.refresh_resume_list()

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

    def create_generated_resume_controls(self, parent):
        """Create controls for saving/loading generated resumes"""
        controls_card = tk.Frame(parent, bg=COLORS['card_bg'], bd=0)
        controls_card.pack(fill="x", padx=40, pady=(10, 20))

        controls_inner = tk.Frame(controls_card, bg=COLORS['card_bg'])
        controls_inner.pack(padx=30, pady=20)

        # Title
        title = tk.Label(
            controls_inner,
            text="Manage Generated Resume",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS['coral'],
            bg=COLORS['card_bg']
        )
        title.pack(anchor="w", pady=(0, 12))

        # Buttons row
        button_row = tk.Frame(controls_inner, bg=COLORS['card_bg'])
        button_row.pack(fill="x")

        # Save generated resume button
        save_gen_btn = ModernButton(
            button_row,
            " Save Generated",
            self.save_generated_resume,
            bg_color="#F472B6",
            hover_color="#EC4899",
            width=160,
            height=45
        )
        save_gen_btn.pack(side="left", padx=(0, 10))

        # Load generated resume section
        load_frame = tk.Frame(button_row, bg=COLORS['card_bg'])
        load_frame.pack(side="left", padx=(10, 0))

        load_label = tk.Label(
            load_frame,
            text="Load:",
            font=("Segoe UI", 10),
            fg=COLORS['text_secondary'],
            bg=COLORS['card_bg']
        )
        load_label.pack(side="left", padx=(0, 8))

        self.generated_var = tk.StringVar()
        self.generated_dropdown = ttk.Combobox(
            load_frame,
            textvariable=self.generated_var,
            state="readonly",
            width=35,
            font=("Segoe UI", 10)
        )
        self.generated_dropdown.pack(side="left", padx=(0, 10))

        load_gen_btn = ModernButton(
            load_frame,
            "📖 Load",
            self.load_generated_resume,
            bg_color="#C084FC",
            hover_color="#A855F7",
            width=90,
            height=35
        )
        load_gen_btn.pack(side="left", padx=(0, 10))

        refresh_gen_btn = ModernButton(
            load_frame,
            "🔄",
            self.refresh_generated_list,
            bg_color="#6EE7B7",
            hover_color="#34D399",
            width=40,
            height=35
        )
        refresh_gen_btn.pack(side="left")

        # PDF Export button
        pdf_frame = tk.Frame(controls_inner, bg=COLORS['card_bg'])
        pdf_frame.pack(pady=(15, 0))

        self.save_btn = ModernButton(
            pdf_frame,
            "💾 Export as PDF",
            self.save_to_pdf,
            bg_color="#10B981",
            hover_color="#059669",
            width=180,
            height=45
        )
        self.save_btn.pack()

        # Load initial list
        self.refresh_generated_list()

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

    def save_current_resume(self):
        """Save the current resume to database"""
        # grab all the form data
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        education = self.education_text.get("1.0", tk.END).strip()
        skills = self.skills_text.get("1.0", tk.END).strip()
        experience = self.experience_text.get("1.0", tk.END).strip()

        if not name:
            messagebox.showwarning("💭 Oops!", "Please enter your name before saving!")
            return

        data = {
            'name': name,
            'email': email,
            'phone': phone,
            'education': education,
            'skills': skills,
            'experience': experience,
        }

        try:
            resume_id = self.db.save_resume(data)
            print(f"Saved resume #{resume_id}")
            messagebox.showinfo("💖 Saved!", f"Your resume has been saved! ✨\n\nResume ID: #{resume_id}")
            self.refresh_resume_list()
            self.status_label.config(text="💝 Resume saved to database!", fg="#E879F9")
        except Exception as e:
            messagebox.showerror("😢 Oops!", f"Couldn't save the resume: {str(e)}")

    def load_selected_resume(self):
        """Load the selected resume from database"""
        selected = self.resume_var.get()

        if not selected:
            messagebox.showinfo("💭 Hey!", "Please select a resume from the dropdown first! ✨")
            return

        # get the ID from selection (format: "ID: Name")
        try:
            resume_id = int(selected.split(':')[0].strip())
        except:
            messagebox.showerror("😕 Hmm...", "Something went wrong with your selection!")
            return

        try:
            data = self.db.load_resume(resume_id)

            if data:
                # fill all the form fields
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, data['name'])

                self.email_entry.delete(0, tk.END)
                self.email_entry.insert(0, data['email'])

                self.phone_entry.delete(0, tk.END)
                self.phone_entry.insert(0, data['phone'])

                self.education_text.delete("1.0", tk.END)
                self.education_text.insert("1.0", data['education'])

                self.skills_text.delete("1.0", tk.END)
                self.skills_text.insert("1.0", data['skills'])

                self.experience_text.delete("1.0", tk.END)
                self.experience_text.insert("1.0", data['experience'])

                self.status_label.config(text=f"✨ Loaded resume #{resume_id}!", fg="#A78BFA")
                messagebox.showinfo("🎉 Loaded!", f"Your resume is ready to edit! 💜")
            else:
                messagebox.showwarning("😢 Not Found", "Couldn't find that resume in the database...")
        except Exception as e:
            messagebox.showerror("😢 Oops!", f"Failed to load resume: {str(e)}")

    def refresh_resume_list(self):
        """Refresh the dropdown list of saved resumes"""
        try:
            resumes = self.db.get_all_resumes()

            # format as "ID: Name (Date)"
            resume_list = []
            for resume in resumes:
                resume_id = resume[0]
                name = resume[1]
                updated_at = resume[2][:10] if len(resume[2]) >= 10 else resume[2]  # just the date part
                resume_list.append(f"{resume_id}: {name} ({updated_at})")

            self.resume_dropdown['values'] = resume_list

            if resume_list:
                self.resume_dropdown.current(0)
        except Exception as e:
            print(f"Failed to refresh resume list: {str(e)}")

    def save_generated_resume(self):
        """Save the generated resume content to database"""
        resume_text = self.output_text.get("1.0", tk.END).strip()

        if not resume_text:
            messagebox.showwarning("💭 Oops!", "No generated resume to save! Generate one first! ✨")
            return

        # ask for a title
        title = tk.simpledialog.askstring(
            "💝 Save Generated Resume",
            "Enter a title for this resume:",
            parent=self.root
        )

        if not title:
            return

        try:
            mode = self.mode_var.get()
            resume_id = self.db.save_generated_resume(title, resume_text, mode)
            print(f"Saved generated resume #{resume_id}")
            messagebox.showinfo("💖 Saved!", f"Generated resume saved! ✨\n\nID: #{resume_id}")
            self.refresh_generated_list()
            self.status_label.config(text="💗 Generated resume saved!", fg="#F472B6")
        except Exception as e:
            messagebox.showerror("😢 Oops!", f"Failed to save: {str(e)}")

    def load_generated_resume(self):
        """Load a saved generated resume"""
        selected = self.generated_var.get()

        if not selected:
            messagebox.showinfo("💭 Hey!", "Please select a resume from the dropdown first! ✨")
            return

        # get ID from selection
        try:
            resume_id = int(selected.split(':')[0].strip())
        except:
            messagebox.showerror("😕 Hmm...", "Something went wrong with your selection!")
            return

        try:
            data = self.db.load_generated_resume(resume_id)

            if data:
                # load the content into output area
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", data['content'])

                mode_info = f" ({data['mode']} mode)" if data.get('mode') else ""
                self.status_label.config(text=f"✨ Loaded: {data['title']}{mode_info}", fg="#C084FC")
                messagebox.showinfo("🎉 Loaded!", f"Resume loaded!\n\n{data['title']} 💜")
            else:
                messagebox.showwarning("😢 Not Found", "Couldn't find that resume...")
        except Exception as e:
            messagebox.showerror("😢 Oops!", f"Failed to load: {str(e)}")

    def refresh_generated_list(self):
        """Refresh the dropdown of generated resumes"""
        try:
            resumes = self.db.get_all_generated_resumes()

            # format as "ID: Title (Date)"
            resume_list = []
            for resume in resumes:
                resume_id = resume[0]
                title = resume[1]
                created_at = resume[2][:10] if len(resume[2]) >= 10 else resume[2]
                resume_list.append(f"{resume_id}: {title} ({created_at})")

            self.generated_dropdown['values'] = resume_list

            if resume_list:
                self.generated_dropdown.current(0)
        except Exception as e:
            print(f"Failed to refresh generated list: {str(e)}")

