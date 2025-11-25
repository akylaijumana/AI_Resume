import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import threading
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    AutoTokenizer = None
    AutoModelForSeq2SeqLM = None
    torch = None

class ResumeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Generator (Free Version)")
        self.root.geometry("850x750")
        self.root.configure(bg="#f0f0f0")

        self.ai_model = None
        self.ai_tokenizer = None
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
                    text="Downloading AI model (only once, ~1GB)...", fg="orange"))

                # Using FLAN-T5 - better for instruction following
                model_name = "google/flan-t5-base"
                self.ai_tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.ai_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

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
        """Create resume using AI - GENERATES FULL CONTENT based on your input"""

        # AI generates professional summary
        summary = self._ai_generate_summary(education, skills, experience)

        # AI generates detailed experience with achievements you didn't write
        formatted_experience = self._ai_generate_full_experience(experience, skills, education)

        # AI suggests additional relevant skills
        formatted_skills = self._ai_expand_skills(skills, experience, education)

        # AI enhances education with relevant coursework/achievements
        formatted_education = self._ai_enhance_education(education, skills)

        # Build resume with professional structure
        resume = f"""{name.upper()}
{email} | {phone}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL SUMMARY
{summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EDUCATION
{formatted_education}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE COMPETENCIES
{formatted_skills}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL EXPERIENCE
{formatted_experience}"""

        return resume

    def _ai_generate_summary(self, education, skills, experience):
        """AI generates a professional summary"""
        try:
            prompt = f"Write a professional 3-sentence resume summary for someone with education: {education[:100]}, skills: {skills[:100]}, experience: {experience[:150]}"

            inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.ai_model.generate(
                inputs.input_ids,
                max_length=120,
                min_length=50,
                temperature=0.8,
                do_sample=True,
                top_p=0.9,
                num_return_sequences=1
            )
            summary = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Validate AI output
            if len(summary) > 40 and len(summary) < 500:
                return summary
        except Exception as e:
            print(f"AI summary failed: {e}")

        # Fallback to template
        return self.generate_summary(experience, skills)

    def _ai_generate_full_experience(self, experience, skills, education):
        """AI CREATES detailed work experience with achievements"""
        if not experience:
            return "• Actively seeking opportunities to apply skills and contribute to organizational success\n• Prepared to leverage education and technical abilities in a professional environment"

        # Parse what user wrote
        lines = [line.strip() for line in experience.split('\n') if line.strip()]
        result = []

        for line in lines:
            # If it's a job title/company, keep it
            if len(line) < 100 and not line.startswith('•') and not line.startswith('-'):
                if result:
                    result.append("")  # spacing
                result.append(line.upper())

                # AI GENERATES responsibilities for this job
                generated_bullets = self._ai_generate_job_responsibilities(line, skills, education)
                result.extend(generated_bullets)
            else:
                # User wrote a responsibility - enhance it with AI
                enhanced = self._ai_enhance_bullet(line, skills)
                if not enhanced.startswith('•'):
                    result.append(f"  • {enhanced}")
                else:
                    result.append(f"  {enhanced}")

        return '\n'.join(result)

    def _ai_generate_job_responsibilities(self, job_title, skills, education):
        """AI GENERATES 3-5 professional responsibilities for a job title"""
        try:
            prompt = f"List 4 professional job responsibilities for: {job_title}. Skills: {skills[:80]}"

            inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=256, truncation=True)
            outputs = self.ai_model.generate(
                inputs.input_ids,
                max_length=150,
                min_length=40,
                temperature=0.7,
                do_sample=True,
                num_return_sequences=1
            )
            ai_response = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Parse AI response into bullets
            bullets = []
            for line in ai_response.split('\n'):
                line = line.strip()
                if line and len(line) > 10:
                    # Clean up and format
                    line = line.lstrip('•-123456789. ')
                    if len(line) > 15 and len(line) < 200:
                        bullets.append(f"  • {line}")

            # If AI generated good bullets, use them
            if len(bullets) >= 2:
                return bullets[:4]

        except Exception as e:
            print(f"AI job responsibilities failed: {e}")

        # Fallback: generate template bullets based on job title
        return self._generate_template_responsibilities(job_title, skills)

    def _generate_template_responsibilities(self, job_title, skills):
        """Generate template responsibilities based on job title"""
        job_lower = job_title.lower()
        skill_list = [s.strip() for s in skills.split(',')[:3]] if skills else []

        bullets = []

        # Add skill-based responsibilities
        if skill_list:
            bullets.append(f"  • Applied expertise in {', '.join(skill_list)} to deliver high-quality results")

        # Add role-specific responsibilities
        if any(word in job_lower for word in ['developer', 'engineer', 'programmer']):
            bullets.extend([
                "  • Developed and maintained software applications using modern technologies",
                "  • Collaborated with cross-functional teams to deliver projects on schedule",
                "  • Implemented best practices for code quality and testing"
            ])
        elif any(word in job_lower for word in ['manager', 'lead', 'supervisor']):
            bullets.extend([
                "  • Led team initiatives and coordinated project deliverables",
                "  • Managed stakeholder relationships and communication",
                "  • Improved team efficiency through process optimization"
            ])
        elif any(word in job_lower for word in ['analyst', 'data']):
            bullets.extend([
                "  • Analyzed complex data sets to drive business insights",
                "  • Created comprehensive reports and visualizations for stakeholders",
                "  • Identified trends and opportunities for operational improvements"
            ])
        elif any(word in job_lower for word in ['designer', 'creative']):
            bullets.extend([
                "  • Designed and delivered creative solutions for client projects",
                "  • Collaborated with stakeholders to understand requirements",
                "  • Maintained brand consistency across all deliverables"
            ])
        else:
            bullets.extend([
                "  • Contributed to team objectives and organizational goals",
                "  • Demonstrated strong problem-solving and analytical skills",
                "  • Collaborated effectively with colleagues and stakeholders"
            ])

        return bullets[:4]

    def _ai_enhance_bullet(self, bullet, skills):
        """AI enhances a user-written bullet point"""
        # Remove existing bullet markers
        cleaned = bullet.lstrip('•- \t')

        if len(cleaned) < 100:  # Only enhance short bullets
            try:
                prompt = f"Make this work achievement more professional and detailed: {cleaned}"

                inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=256, truncation=True)
                outputs = self.ai_model.generate(
                    inputs.input_ids,
                    max_length=80,
                    min_length=20,
                    temperature=0.7,
                    do_sample=True
                )
                enhanced = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True)

                if len(enhanced) > len(cleaned) and len(enhanced) < 250:
                    return enhanced
            except:
                pass

        return cleaned

    def _ai_expand_skills(self, skills, experience, education):
        """AI suggests additional relevant skills based on experience/education"""
        base_skills = self.format_skills(skills)

        # AI generates additional skills
        try:
            prompt = f"List 5 relevant professional skills for someone with experience: {experience[:100]} and education: {education[:80]}"

            inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=256, truncation=True)
            outputs = self.ai_model.generate(
                inputs.input_ids,
                max_length=100,
                min_length=20,
                temperature=0.6,
                do_sample=True
            )
            ai_skills = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Parse AI suggestions
            suggested = []
            for line in ai_skills.split(','):
                skill = line.strip().lstrip('•-123456789. ')
                if skill and len(skill) > 3 and len(skill) < 50:
                    suggested.append(skill)

            if suggested:
                result = base_skills + "\n\nAdditional Strengths: " + ", ".join(suggested[:5])
                return result
        except:
            pass

        return base_skills

    def _ai_enhance_education(self, education, skills):
        """AI adds relevant details to education"""
        if not education:
            return "• Education details to be provided"

        formatted = self.format_education(education)

        # Try to add relevant coursework based on skills
        try:
            if skills:
                prompt = f"List 3 relevant courses for degree: {education[:100]} with skills: {skills[:80]}"

                inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=256, truncation=True)
                outputs = self.ai_model.generate(
                    inputs.input_ids,
                    max_length=80,
                    min_length=15,
                    temperature=0.6
                )
                courses = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True)

                if courses and len(courses) > 20:
                    formatted += f"\n  Relevant Coursework: {courses}"
        except:
            pass

        return formatted

    def create_professional_resume(self, name, email, phone, education, skills, experience):
        """Generate a professional resume - also adds extra content based on your info"""

        # Create professional summary based on experience and skills
        summary = self.generate_summary(experience, skills)

        # Format skills professionally and add suggested skills
        formatted_skills = self.format_skills_with_suggestions(skills, experience, education)

        # Format experience with AUTO-GENERATED responsibilities
        formatted_experience = self.format_experience_with_generation(experience, skills)

        # Format education
        formatted_education = self.format_education(education)

        # Build the complete resume with professional structure
        resume = f"""{name.upper()}
{email} | {phone}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL SUMMARY
{summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EDUCATION
{formatted_education}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE COMPETENCIES
{formatted_skills}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL EXPERIENCE
{formatted_experience}"""

        return resume

    def format_skills_with_suggestions(self, skills, experience, education):
        """Format skills and ADD suggested skills based on experience"""
        base_skills = self.format_skills(skills)

        # Auto-suggest skills based on experience keywords
        suggested = []
        exp_lower = experience.lower() if experience else ""
        edu_lower = education.lower() if education else ""

        # Check for common tech roles
        if any(word in exp_lower or word in edu_lower for word in ['developer', 'software', 'programming', 'computer science']):
            suggested.extend(['Problem-solving', 'Debugging', 'Code review', 'Version control'])

        if any(word in exp_lower or word in edu_lower for word in ['data', 'analyst', 'analytics']):
            suggested.extend(['Data analysis', 'Statistical thinking', 'Report generation', 'Data visualization'])

        if any(word in exp_lower or word in edu_lower for word in ['manager', 'lead', 'supervisor']):
            suggested.extend(['Team leadership', 'Project management', 'Stakeholder communication', 'Strategic planning'])

        if any(word in exp_lower or word in edu_lower for word in ['designer', 'design', 'creative']):
            suggested.extend(['Creative thinking', 'Visual design', 'User experience', 'Attention to detail'])

        # Add general professional skills
        if not any(word in skills.lower() for word in ['communication', 'teamwork', 'collaboration']):
            suggested.extend(['Effective communication', 'Team collaboration'])

        # Remove duplicates and limit
        skill_lower = skills.lower()
        unique_suggested = [s for s in suggested if s.lower() not in skill_lower][:6]

        if unique_suggested:
            return base_skills + "\n\nAdditional Strengths: " + ", ".join(unique_suggested)

        return base_skills

    def format_experience_with_generation(self, experience, skills):
        """Format experience and AUTO-ADD professional responsibilities"""
        if not experience:
            return "• Actively seeking opportunities to apply skills and contribute to organizational success\n• Prepared to leverage education and expertise in a professional environment"

        lines = [line.strip() for line in experience.split('\n') if line.strip()]
        formatted = []
        current_job = None

        for line in lines:
            # Check if line looks like a job title/company
            if len(line) < 100 and not line.startswith('•') and not line.startswith('-'):
                # Likely a job title
                if formatted:
                    formatted.append("")  # Add spacing between jobs
                formatted.append(line.upper())
                current_job = line
            else:
                # Responsibility line
                if not line.startswith('•') and not line.startswith('-'):
                    formatted.append(f"  • {line}")
                else:
                    formatted.append(f"  {line}")

        # AUTO-ADD responsibilities if user only provided job titles
        result = []
        i = 0
        while i < len(formatted):
            line = formatted[i]
            result.append(line)

            # If this is a job title and next line is another job title or end, ADD responsibilities
            if line and line.isupper() and (i + 1 >= len(formatted) or (i + 1 < len(formatted) and formatted[i + 1].isupper())):
                # User didn't write responsibilities - generate them!
                auto_bullets = self._generate_template_responsibilities(line, skills)
                result.extend(auto_bullets)

            i += 1

        return '\n'.join(result)

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

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="resume.pdf"
        )

        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)

            elements = []

            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='CustomBody',
                                     parent=styles['BodyText'],
                                     fontSize=10,
                                     leading=14))

            paragraphs = resume_text.split('\n')
            for para in paragraphs:
                if para.strip():
                    if para.isupper() or len(para) < 40:
                        p = Paragraph(para, styles['Heading2'])
                    else:
                        p = Paragraph(para, styles['CustomBody'])
                    elements.append(p)
                    elements.append(Spacer(1, 0.1*inch))

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

