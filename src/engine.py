"""
Resume Generation Engine
Handles both template-based and AI-powered resume generation
"""
import random
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


class ResumeEngine:
    """Core resume generation engine"""

    def __init__(self):
        self.ai_model = None
        self.ai_tokenizer = None
        self.model_loaded = False

    def load_ai_model(self):
        """Load AI model for enhanced generation"""
        if not AI_AVAILABLE:
            return False

        try:
            if not self.model_loaded:
                self.ai_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
                self.ai_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
                self.model_loaded = True
            return True
        except Exception as e:
            print(f"Failed to load AI model: {e}")
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
            context = f"Education: {education}\nSkills: {skills}\nExperience: {experience[:200]}"
            prompt = f"Write a professional 3-sentence resume summary for someone with: {context}"

            inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.ai_model.generate(
                inputs.input_ids,
                max_length=150,
                min_length=50,
                temperature=0.7,
                do_sample=True,
                top_p=0.95,
            )

            summary = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True)

            if len(summary) > 100 and len(summary) < 500:
                return summary
        except:
            pass

        return self.generate_summary(education, skills, experience)

    def ai_generate_full_experience(self, experience, skills, education):
        """Generate AI-enhanced experience section"""
        if not experience.strip():
            return "  • Ready to bring dedication and skills to a new role"

        lines = [line.strip() for line in experience.split('\n') if line.strip()]
        formatted = []
        current_job = None

        for line in lines:
            if len(line) < 100 and not line.startswith(('•', '-', '  ')):
                current_job = line
                formatted.append(f"\n{line.upper()}" if formatted else line.upper())
            else:
                responsibilities = self.ai_generate_job_responsibilities(
                    current_job or "Professional", skills, education
                )
                if responsibilities:
                    formatted.extend(responsibilities)
                    current_job = None

        return '\n'.join(formatted) if formatted else self.format_experience(experience, skills)

    def ai_generate_job_responsibilities(self, job_title, skills, education):
        """Generate AI-powered job responsibilities"""
        try:
            prompt = f"List 4 professional achievements for a {job_title} with skills in {skills[:100]}"

            inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=256, truncation=True)
            outputs = self.ai_model.generate(
                inputs.input_ids,
                max_length=200,
                min_length=50,
                temperature=0.8,
                do_sample=True,
                num_beams=4,
            )

            result = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True)
            bullets = [f"  • {line.strip()}" for line in result.split('\n') if line.strip()]

            if bullets and len(bullets) >= 2:
                return bullets[:4]
        except:
            pass

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

