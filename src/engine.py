"""
Resume Generation Engine
Handles both template-based and AI-powered resume generation
"""
import random
import warnings
import os

# Suppress all warnings for cleaner output
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'  # Disable Hugging Face telemetry

# Check AI availability without importing (faster startup)
AI_AVAILABLE = False
try:
    import importlib.util
    if importlib.util.find_spec("transformers") is not None:
        AI_AVAILABLE = True
except:
    AI_AVAILABLE = False


class ResumeEngine:
    """Core resume generation engine"""

    def __init__(self):
        self.ai_model = None
        self.ai_tokenizer = None
        self.model_loaded = False

    def load_ai_model(self):
        """Load AI model for enhanced generation"""
        if not AI_AVAILABLE:
            print("AI libraries not available")
            return False

        try:
            if not self.model_loaded:
                print("Loading AI model... (this may take a moment)")

                # Import only when needed (lazy loading for faster startup)
                from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
                import logging

                # Suppress transformers logging but not errors
                logging.getLogger("transformers").setLevel(logging.ERROR)

                # Using FLAN-T5 - better for instruction following (ORIGINAL MODEL)
                model_name = "google/flan-t5-base"
                self.ai_tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.ai_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                self.model_loaded = True
                print("AI model loaded successfully!")
            return True
        except Exception as e:
            print(f"Failed to load AI model: {str(e)}")
            return False

    def generate_resume(self, data, mode='template'):
        """
        Generate resume content

        Args:
            data: dict with keys: name, email, phone, education, skills, experience
            mode: 'template' or 'ai'

        Returns:
            str: Formatted resume text
        """
        if mode == 'ai' and AI_AVAILABLE:
            return self.create_ai_resume(data)
        else:
            return self.create_template_resume(data)

    def create_template_resume(self, data):
        """Generate resume using templates"""
        resume = []

        # Header
        resume.append(data['name'].upper())
        resume.append(f"{data['email']} | {data['phone']}")
        resume.append("=" * 80)
        resume.append("")

        # Professional Summary
        summary = self.generate_summary(data['education'], data['skills'], data['experience'])
        resume.append("PROFESSIONAL SUMMARY")
        resume.append("-" * 80)
        resume.append(summary)
        resume.append("")

        # Skills
        resume.append("SKILLS")
        resume.append("-" * 80)
        resume.append(self.format_skills(data['skills']))
        resume.append("")

        # Experience
        resume.append("PROFESSIONAL EXPERIENCE")
        resume.append("-" * 80)
        resume.append(self.format_experience(data['experience'], data['skills']))
        resume.append("")

        # Education
        resume.append("EDUCATION")
        resume.append("-" * 80)
        resume.append(self.format_education(data['education']))

        return '\n'.join(resume)

    def create_ai_resume(self, data):
        """Generate AI-enhanced resume"""
        if not self.model_loaded:
            if not self.load_ai_model():
                return self.create_template_resume(data)

        resume = []

        # Header
        resume.append(data['name'].upper())
        resume.append(f"{data['email']} | {data['phone']}")
        resume.append("=" * 80)
        resume.append("")

        # AI-Enhanced Summary
        resume.append("PROFESSIONAL SUMMARY")
        resume.append("-" * 80)
        ai_summary = self.ai_generate_summary(data['education'], data['skills'], data['experience'])
        resume.append(ai_summary)
        resume.append("")

        # Skills
        resume.append("CORE COMPETENCIES")
        resume.append("-" * 80)
        resume.append(self.format_skills(data['skills']))
        resume.append("")

        # AI-Enhanced Experience
        resume.append("PROFESSIONAL EXPERIENCE")
        resume.append("-" * 80)
        ai_experience = self.ai_generate_full_experience(
            data['experience'], data['skills'], data['education']
        )
        resume.append(ai_experience)
        resume.append("")

        # Education
        resume.append("EDUCATION")
        resume.append("-" * 80)
        resume.append(self.format_education(data['education']))

        return '\n'.join(resume)

    def generate_summary(self, education, skills, experience):
        """Generate professional summary"""
        skill_list = [s.strip() for s in skills.replace('\n', ',').split(',') if s.strip()]
        top_skills = ', '.join(skill_list[:3]) if skill_list else "various technical and professional skills"

        exp_lines = [line for line in experience.split('\n') if line.strip()]
        has_experience = len(exp_lines) > 2

        if has_experience:
            summary = f"Results-driven professional with expertise in {top_skills}. "
            summary += "Proven track record of delivering high-quality solutions and driving organizational success. "
            summary += "Strong analytical and problem-solving abilities with excellent communication skills."
        else:
            summary = f"Motivated professional with strong foundation in {top_skills}. "
            summary += "Quick learner with excellent analytical and communication skills. "
            summary += "Seeking to contribute skills and grow professionally in a dynamic environment."

        return summary

    def ai_generate_summary(self, education, skills, experience):
        """AI-generated professional summary"""
        try:
            # Extract key info
            skill_list = [s.strip() for s in skills.replace('\n', ',').split(',') if s.strip()][:5]
            skills_text = ', '.join(skill_list) if skill_list else "various skills"

            # Simple, direct prompt for FLAN-T5
            prompt = f"""Write a professional resume summary (2-3 sentences) for someone with:
- Education: {education[:80]}
- Skills: {skills_text}
- Experience: {experience[:100]}

The summary should highlight their strengths and career goals."""

            print(f"Generating AI summary...")
            inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=400, truncation=True)
            outputs = self.ai_model.generate(
                inputs.input_ids,
                max_length=180,
                min_length=30,
                temperature=0.85,
                do_sample=True,
                top_p=0.90,
                repetition_penalty=1.4,
            )

            summary = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

            print(f"Raw AI summary: {summary}")

            # Clean up - remove prompt repetition
            if summary.lower().startswith(('write', 'create', 'summary', 'the summary')):
                # Try to extract actual content after colon or newline
                parts = summary.split(':', 1)
                if len(parts) > 1:
                    summary = parts[1].strip()
                else:
                    parts = summary.split('\n', 1)
                    if len(parts) > 1:
                        summary = parts[1].strip()

            # Remove any remaining instruction artifacts
            summary = summary.replace('Write a professional resume summary', '').replace('(2-3 sentences)', '').strip()

            # Validate the cleaned output
            if len(summary) > 40 and len(summary) < 500:
                print(f"✓ AI generated summary: {summary[:100]}...")
                return summary
            else:
                print(f"✗ AI summary too short/long ({len(summary)} chars), using template")
        except Exception as e:
            print(f"AI summary generation failed: {str(e)}")

        return self.generate_summary(education, skills, experience)

    def ai_generate_full_experience(self, experience, skills, education):
        """Generate AI-enhanced experience section"""
        if not experience.strip():
            return "  • Ready to bring dedication and skills to a new role"

        lines = [line.strip() for line in experience.split('\n') if line.strip()]
        formatted = []
        current_job = None
        i = 0

        while i < len(lines):
            line = lines[i]

            # Detect job titles (short lines, no bullets, usually company/title)
            if len(line) < 100 and not line.startswith(('•', '-', '  ')):
                # This is a job title or company
                if formatted:
                    formatted.append("")  # Blank line between jobs
                formatted.append(line.upper())
                current_job = line

                # Generate AI responsibilities for this job
                print(f"\nGenerating AI content for: {current_job}")
                responsibilities = self.ai_generate_job_responsibilities(
                    current_job, skills, education
                )
                formatted.extend(responsibilities)

                # Skip any existing bullet points for this job (we generated new ones)
                i += 1
                while i < len(lines) and (lines[i].startswith(('•', '-', '  ')) or len(lines[i]) > 100):
                    i += 1
                continue

            i += 1

        result = '\n'.join(formatted) if formatted else self.format_experience(experience, skills)
        print(f"\nGenerated experience section ({len(result)} chars)")
        return result

    def ai_generate_job_responsibilities(self, job_title, skills, education):
        """Generate AI-powered job responsibilities"""
        try:
            # FLAN-T5 works best with clear, simple instructions
            skills_text = skills[:100] if skills else "various professional skills"

            # Simpler prompt that FLAN-T5 can handle better
            prompt = f"""Create 4 professional resume bullet points for a {job_title} position using these skills: {skills_text}

Each bullet point should describe an achievement or responsibility. Be specific and use action verbs."""

            print(f"Generating AI responsibilities for: {job_title}...")

            inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=400, truncation=True)
            outputs = self.ai_model.generate(
                inputs.input_ids,
                max_length=250,
                min_length=60,
                temperature=0.95,
                do_sample=True,
                top_p=0.92,
                repetition_penalty=1.5,
                no_repeat_ngram_size=2,
                num_return_sequences=1,
            )

            result = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

            print(f"Raw AI output: {result[:200]}...")

            # Clean up the output - FLAN-T5 sometimes repeats the prompt
            # Remove the prompt if it appears in the output
            lines_to_check = result.split('\n')
            clean_lines = []

            for line in lines_to_check:
                line = line.strip()
                # Skip lines that are just repeating the prompt
                if any(skip in line.lower() for skip in ['create', 'bullet point', 'resume', 'should describe', 'each bullet']):
                    continue
                # Remove common bullet markers and numbering
                line = line.lstrip('•-*1234567890. ')
                # Keep lines that look like actual content
                if len(line) > 15 and len(line) < 300:
                    clean_lines.append(line)

            # Format as bullets
            bullets = [f"  • {line}" for line in clean_lines]

            # If we didn't get enough bullets, try splitting by common patterns
            if len(bullets) < 2:
                # Try splitting on periods or common separators
                sentences = result.replace('. ', '.|').split('|')
                bullets = []
                for sent in sentences:
                    sent = sent.strip().strip('.')
                    if len(sent) > 20 and len(sent) < 250 and not any(skip in sent.lower() for skip in ['create', 'bullet', 'write', 'describe']):
                        bullets.append(f"  • {sent}")

            # If we got good bullets, use them
            if len(bullets) >= 2:
                print(f"✓ AI generated {len(bullets)} creative bullets!")
                return bullets[:4]
            else:
                print(f"✗ AI output didn't produce valid bullets, using template")

        except Exception as e:
            print(f"AI generation error: {str(e)}")

        return self.generate_template_responsibilities(job_title, skills)

    def generate_template_responsibilities(self, job_title, skills):
        """Generate template-based responsibilities"""
        job_lower = job_title.lower() if job_title else ""
        skill_list = [s.strip() for s in skills.split(',')[:3]] if skills else []

        random.seed(hash(job_title))
        bullets = []

        if any(word in job_lower for word in ['developer', 'engineer', 'programmer', 'software']):
            dev_bullets = [
                "  • Developed and maintained software applications using modern technologies and frameworks",
                "  • Designed and implemented scalable solutions to meet business requirements",
                "  • Collaborated with cross-functional teams to deliver projects on schedule",
                "  • Participated in code reviews and maintained high code quality standards",
                "  • Optimized database queries and improved application performance by 30%",
                "  • Implemented best practices for code quality, testing, and documentation",
            ]
            bullets.extend(random.sample(dev_bullets, min(4, len(dev_bullets))))

        elif any(word in job_lower for word in ['manager', 'lead', 'supervisor', 'director']):
            mgmt_bullets = [
                "  • Led team initiatives and coordinated project deliverables across departments",
                "  • Managed cross-functional teams to achieve strategic objectives",
                "  • Improved team efficiency through process optimization and automation",
                "  • Developed and executed strategic plans aligned with company goals",
                "  • Mentored team members and fostered professional development",
                "  • Built and maintained relationships with key stakeholders and clients",
            ]
            bullets.extend(random.sample(mgmt_bullets, min(4, len(mgmt_bullets))))

        elif any(word in job_lower for word in ['analyst', 'data', 'research']):
            analyst_bullets = [
                "  • Analyzed complex data sets to drive business insights and recommendations",
                "  • Created comprehensive reports and visualizations for stakeholders",
                "  • Identified trends and opportunities for operational improvements",
                "  • Collaborated with business units to define metrics and reporting requirements",
                "  • Automated reporting processes to improve efficiency and accuracy",
                "  • Maintained data quality and integrity across multiple systems",
            ]
            bullets.extend(random.sample(analyst_bullets, min(4, len(analyst_bullets))))

        elif any(word in job_lower for word in ['designer', 'creative', 'ui', 'ux']):
            design_bullets = [
                "  • Created user-centered designs that improved engagement and satisfaction",
                "  • Collaborated with stakeholders to understand requirements and objectives",
                "  • Maintained brand consistency across all deliverables and touchpoints",
                "  • Produced wireframes, mockups, and prototypes for new features",
                "  • Conducted user research and usability testing to inform design decisions",
                "  • Managed multiple design projects with competing deadlines",
            ]
            bullets.extend(random.sample(design_bullets, min(4, len(design_bullets))))

        else:
            generic_bullets = [
                "  • Contributed to team objectives and organizational goals",
                "  • Demonstrated strong problem-solving and analytical skills",
                "  • Collaborated effectively with colleagues and stakeholders",
                "  • Managed multiple priorities in fast-paced environment",
                "  • Maintained excellent communication with internal and external partners",
                "  • Provided excellent customer service and support",
            ]
            bullets.extend(random.sample(generic_bullets, min(4, len(generic_bullets))))

        if skill_list and len(bullets) < 4:
            bullets.insert(0, f"  • Utilized {', '.join(skill_list[:2])} to deliver high-quality results")

        random.seed()
        return bullets[:4]

    def format_skills(self, skills):
        """Format skills section"""
        if not skills:
            return "• To be added based on role requirements"

        skill_list = [s.strip() for s in skills.replace('\n', ',').split(',') if s.strip()]

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

    def format_experience(self, experience, skills=""):
        """Format experience section"""
        if not experience:
            return "• Ready to bring dedication and skills to a new role"

        lines = [line.strip() for line in experience.split('\n') if line.strip()]
        formatted = []

        for line in lines:
            if len(line) < 100 and not line.startswith(('•', '-')):
                formatted.append(f"\n{line.upper()}" if formatted else line.upper())
            else:
                if not line.startswith(('•', '-')):
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
            if not line.startswith(('•', '-')):
                formatted.append(f"• {line}")
            else:
                formatted.append(line)

        return '\n'.join(formatted)

