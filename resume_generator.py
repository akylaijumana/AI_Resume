import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import threading
import warnings
warnings.filterwarnings('ignore')

# Try to import AI libraries (optional - only needed for AI mode)
try:
    from transformers import pipeline
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    pipeline = None

class ResumeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Generator (Free Version)")
        self.root.geometry("850x750")
        self.root.configure(bg="#f0f0f0")

        # AI model (loaded on demand)
        self.ai_model = None
        self.model_loaded = False

        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Title
        title_label = tk.Label(main_frame, text="AI Resume Generator",
                              font=("Arial", 20, "bold"), bg="#f0f0f0")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Mode Selection
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(mode_frame, text="Generation Mode:", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        self.mode_var = tk.StringVar(value="template")
        ttk.Radiobutton(mode_frame, text="Template (Fast)", variable=self.mode_var,
                       value="template").pack(side="left", padx=5)

        # Only show AI option if libraries are installed
        if AI_AVAILABLE:
            ttk.Radiobutton(mode_frame, text="AI (Better Quality, Slower)", variable=self.mode_var,
                           value="ai").pack(side="left", padx=5)
        else:
            ttk.Label(mode_frame, text="(AI mode: Install transformers & torch)",
                     font=("Arial", 8), foreground="gray").pack(side="left", padx=5)

        # Status label
        self.status_label = tk.Label(main_frame, text="Ready",
                                    font=("Arial", 9), fg="green", bg="#f0f0f0")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Input fields
        row = 3

        # Name
        ttk.Label(main_frame, text="Full Name:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=50)
        self.name_entry.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        # Email
        ttk.Label(main_frame, text="Email:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(main_frame, width=50)
        self.email_entry.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        # Phone
        ttk.Label(main_frame, text="Phone:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(main_frame, width=50)
        self.phone_entry.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        # Education
        ttk.Label(main_frame, text="Education:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.education_text = scrolledtext.ScrolledText(main_frame, width=50, height=3)
        self.education_text.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        # Skills
        ttk.Label(main_frame, text="Skills:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.skills_text = scrolledtext.ScrolledText(main_frame, width=50, height=3)
        self.skills_text.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        # Experience
        ttk.Label(main_frame, text="Experience:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.experience_text = scrolledtext.ScrolledText(main_frame, width=50, height=4)
        self.experience_text.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        # Generate Button
        self.generate_btn = tk.Button(main_frame, text="Generate Resume",
                                     command=self.generate_resume,
                                     bg="#4CAF50", fg="white",
                                     font=("Arial", 12, "bold"),
                                     padx=20, pady=10)
        self.generate_btn.grid(row=row, column=0, columnspan=2, pady=20)
        row += 1

        # Output area
        ttk.Label(main_frame, text="Generated Resume:").grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.output_text = scrolledtext.ScrolledText(main_frame, width=70, height=10)
        self.output_text.grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        row += 1

        # Save Button
        self.save_btn = tk.Button(main_frame, text="Save as PDF",
                                 command=self.save_to_pdf,
                                 bg="#2196F3", fg="white",
                                 font=("Arial", 10, "bold"),
                                 padx=15, pady=8)
        self.save_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)

    def generate_resume(self):
        # Get input values
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        education = self.education_text.get("1.0", tk.END).strip()
        skills = self.skills_text.get("1.0", tk.END).strip()
        experience = self.experience_text.get("1.0", tk.END).strip()

        # Validate inputs
        if not name or not email:
            messagebox.showwarning("Warning", "Please enter at least your name and email")
            return

        mode = self.mode_var.get()

        if mode == "ai":
            # Check if AI libraries are available
            if not AI_AVAILABLE:
                messagebox.showerror("AI Not Available",
                    "AI mode requires additional packages.\n\n"
                    "Install with:\npip install transformers torch\n\n"
                    "Using Template mode instead.")
                mode = "template"
            else:
                # Use AI mode in background thread
                self.generate_btn.config(state="disabled", text="Loading AI Model...")
                self.status_label.config(text="Loading AI model (first time may take 1-2 minutes)...", fg="orange")
                threading.Thread(target=self._generate_with_ai,
                               args=(name, email, phone, education, skills, experience),
                               daemon=True).start()
                return

        # Use template mode (fast)
        self.generate_btn.config(state="disabled", text="Generating...")
        self.status_label.config(text="Generating...", fg="blue")
        self.root.update()

        try:
            resume_text = self.create_professional_resume(
                name, email, phone, education, skills, experience
            )

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", resume_text)
            self.status_label.config(text="Resume generated successfully!", fg="green")
            messagebox.showinfo("Success", "Resume generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate resume: {str(e)}")
            self.status_label.config(text="Error occurred", fg="red")

        finally:
            self.generate_btn.config(state="normal", text="Generate Resume")

    def _generate_with_ai(self, name, email, phone, education, skills, experience):
        """Generate resume using free AI model in background thread"""
        try:
            # Load model if not already loaded
            if not self.model_loaded:
                self.root.after(0, lambda: self.status_label.config(
                    text="Downloading AI model (only once, ~500MB)...", fg="orange"))

                self.ai_model = pipeline("text-generation",
                                        model="gpt2",
                                        max_length=500,
                                        device=-1)  # Use CPU
                self.model_loaded = True

                self.root.after(0, lambda: self.status_label.config(
                    text="Model loaded! Generating resume...", fg="blue"))
            else:
                self.root.after(0, lambda: self.status_label.config(
                    text="Generating resume with AI...", fg="blue"))

            # Create AI-enhanced resume
            resume_text = self.create_ai_resume(name, email, phone, education, skills, experience)

            # Update UI from main thread
            self.root.after(0, lambda: self.output_text.delete("1.0", tk.END))
            self.root.after(0, lambda: self.output_text.insert("1.0", resume_text))
            self.root.after(0, lambda: self.status_label.config(
                text="AI Resume generated successfully!", fg="green"))
            self.root.after(0, lambda: messagebox.showinfo("Success",
                "AI-powered resume generated successfully!"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error",
                f"AI generation failed: {str(e)}\n\nTry Template mode instead."))
            self.root.after(0, lambda: self.status_label.config(
                text="AI failed - use Template mode", fg="red"))

        finally:
            self.root.after(0, lambda: self.generate_btn.config(
                state="normal", text="Generate Resume"))

    def create_ai_resume(self, name, email, phone, education, skills, experience):
        """Create resume using AI text generation"""

        # Generate AI-enhanced professional summary
        summary_prompt = f"Professional summary for someone with skills in {skills[:100]}: "
        try:
            ai_summary = self.ai_model(summary_prompt,
                                      max_length=150,
                                      num_return_sequences=1,
                                      temperature=0.7,
                                      do_sample=True)[0]['generated_text']
            # Clean up the summary
            summary = ai_summary.replace(summary_prompt, "").strip()
            # Fallback if AI output is weird
            if len(summary) < 20 or len(summary) > 300:
                summary = self.generate_summary(experience, skills)
        except:
            summary = self.generate_summary(experience, skills)

        # Use template formatting for other sections (more reliable)
        formatted_skills = self.format_skills(skills)
        formatted_experience = self.format_experience(experience)
        formatted_education = self.format_education(education)

        # Build resume
        resume = f"""{name.upper()}
{email} | {phone}

PROFESSIONAL SUMMARY
{summary}

EDUCATION
{formatted_education}

SKILLS
{formatted_skills}

PROFESSIONAL EXPERIENCE
{formatted_experience}"""

        return resume

    def create_professional_resume(self, name, email, phone, education, skills, experience):
        """Generate a professional resume without using AI API"""

        # Create professional summary based on experience and skills
        summary = self.generate_summary(experience, skills)

        # Format skills professionally
        formatted_skills = self.format_skills(skills)

        # Format experience with bullet points
        formatted_experience = self.format_experience(experience)

        # Format education
        formatted_education = self.format_education(education)

        # Build the complete resume
        resume = f"""{name.upper()}
{email} | {phone}

PROFESSIONAL SUMMARY
{summary}

EDUCATION
{formatted_education}

SKILLS
{formatted_skills}

PROFESSIONAL EXPERIENCE
{formatted_experience}"""

        return resume

    def generate_summary(self, experience, skills):
        """Generate a professional summary based on input"""
        if not experience and not skills:
            return "Motivated professional seeking new opportunities to leverage skills and contribute to organizational success."

        # Extract key points
        exp_lines = experience.split('\n') if experience else []
        skill_list = [s.strip() for s in skills.split(',') if s.strip()] if skills else []

        # Count years if mentioned
        years = "experienced"
        for line in exp_lines:
            if any(word in line.lower() for word in ['years', 'year']):
                years = "seasoned"
                break

        # Get top skills
        top_skills = ", ".join(skill_list[:3]) if len(skill_list) >= 3 else skills

        if experience:
            summary = f"{years.capitalize()} professional with proven expertise in {top_skills}. "
            summary += "Demonstrated track record of delivering results and contributing to team success. "
            summary += "Strong analytical and problem-solving abilities with excellent communication skills."
        else:
            summary = f"Motivated professional with strong foundation in {top_skills}. "
            summary += "Quick learner with excellent analytical and communication skills. "
            summary += "Seeking to contribute skills and grow professionally in a dynamic environment."

        return summary

    def format_skills(self, skills):
        """Format skills into a professional layout"""
        if not skills:
            return "• To be added based on role requirements"

        # Try to categorize skills
        skill_list = [s.strip() for s in skills.replace('\n', ',').split(',') if s.strip()]

        # Group skills by category if possible
        technical = []
        soft = []

        soft_keywords = ['communication', 'leadership', 'teamwork', 'management',
                        'problem-solving', 'analytical', 'creative', 'collaboration']

        for skill in skill_list:
            if any(keyword in skill.lower() for keyword in soft_keywords):
                soft.append(skill)
            else:
                technical.append(skill)

        result = ""
        if technical:
            result += "Technical Skills: " + ", ".join(technical) + "\n"
        if soft:
            result += "Professional Skills: " + ", ".join(soft)

        if not result:
            result = "• " + "\n• ".join(skill_list)

        return result

    def format_experience(self, experience):
        """Format experience with professional structure"""
        if not experience:
            return "• Ready to bring dedication and skills to a new role"

        lines = [line.strip() for line in experience.split('\n') if line.strip()]
        formatted = []

        for line in lines:
            # Check if line looks like a job title/company (usually first line or short)
            if len(line) < 100 and not line.startswith('•') and not line.startswith('-'):
                # Likely a job title
                formatted.append(f"\n{line.upper()}" if len(formatted) > 0 else line.upper())
            else:
                # Responsibility or achievement
                if not line.startswith('•') and not line.startswith('-'):
                    formatted.append(f"  • {line}")
                else:
                    formatted.append(f"  {line}")

        return '\n'.join(formatted)

    def format_education(self, education):
        """Format education section"""
        if not education:
            return "• Educational background to be provided"

        lines = [line.strip() for line in education.split('\n') if line.strip()]
        formatted = []

        for line in lines:
            if not line.startswith('•') and not line.startswith('-'):
                formatted.append(f"• {line}")
            else:
                formatted.append(line)

        return '\n'.join(formatted)

    def save_to_pdf(self):
        resume_text = self.output_text.get("1.0", tk.END).strip()

        if not resume_text:
            messagebox.showwarning("Warning", "No resume to save. Generate a resume first.")
            return

        # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="resume.pdf"
        )

        if not file_path:
            return

        try:
            # Create PDF
            doc = SimpleDocTemplate(file_path, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)

            # Container for the 'Flowable' objects
            elements = []

            # Define styles
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='CustomBody',
                                     parent=styles['BodyText'],
                                     fontSize=10,
                                     leading=14))

            # Split resume into paragraphs and add to PDF
            paragraphs = resume_text.split('\n')
            for para in paragraphs:
                if para.strip():
                    # Check if it's a header (all caps or short line)
                    if para.isupper() or len(para) < 40:
                        p = Paragraph(para, styles['Heading2'])
                    else:
                        p = Paragraph(para, styles['CustomBody'])
                    elements.append(p)
                    elements.append(Spacer(1, 0.1*inch))

            # Build PDF
            doc.build(elements)

            messagebox.showinfo("Success", f"Resume saved to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")

def main():
    root = tk.Tk()
    app = ResumeGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

