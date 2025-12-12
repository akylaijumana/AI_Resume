"""
Resume Generation Engine
Handles both template-based and AI-powered resume generation
"""
import random
import warnings
import os

# suppress warnings so output looks cleaner
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'

# check if transformers library is available before trying to import it
AI_AVAILABLE = False
try:
    import importlib.util
    spec = importlib.util.find_spec("transformers")
    if spec is not None:
        AI_AVAILABLE = True
except:
    pass


class ResumeEngine:
    """Main engine for generating resumes"""

    def __init__(self):
        self.ai_model = None
        self.ai_tokenizer = None
        self.model_loaded = False

    def load_ai_model(self):
        """Try to load the AI model if transformers library is available"""
        if not AI_AVAILABLE:
            print("AI libraries not available")
            return False

        try:
            # only load once
            if self.model_loaded:
                return True

            print("Loading AI model... (this may take a moment)")

            # import here so startup is faster
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            import logging

            # reduce noise from transformers logging
            logging.getLogger("transformers").setLevel(logging.ERROR)

            # using FLAN-T5 base model - works well for text generation
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

        # header with name and contact info
        name_upper = data['name'].upper()
        resume.append(name_upper)
        contact_line = data['email'] + " | " + data['phone']
        resume.append(contact_line)
        resume.append("=" * 80)
        resume.append("")

        # professional summary section
        summary_text = self.generate_summary(data['education'], data['skills'], data['experience'])
        resume.append("PROFESSIONAL SUMMARY")
        resume.append("-" * 80)
        resume.append(summary_text)
        resume.append("")

        # skills section
        resume.append("SKILLS")
        resume.append("-" * 80)
        skills_formatted = self.format_skills(data['skills'])
        resume.append(skills_formatted)
        resume.append("")

        # work experience section
        resume.append("PROFESSIONAL EXPERIENCE")
        resume.append("-" * 80)
        exp_formatted = self.format_experience(data['experience'], data['skills'])
        resume.append(exp_formatted)
        resume.append("")

        # education section
        resume.append("EDUCATION")
        resume.append("-" * 80)
        edu_formatted = self.format_education(data['education'])
        resume.append(edu_formatted)

        final_resume = '\n'.join(resume)
        return final_resume

    def create_ai_resume(self, data):
        """Generate AI-enhanced resume"""
        # make sure model is loaded first
        if not self.model_loaded:
            loaded_ok = self.load_ai_model()
            if not loaded_ok:
                # fallback to template if AI doesn't work
                return self.create_template_resume(data)

        resume = []

        # put header at top
        resume.append(data['name'].upper())
        contact_info = f"{data['email']} | {data['phone']}"
        resume.append(contact_info)
        resume.append("=" * 80)
        resume.append("")

        # generate AI summary
        resume.append("PROFESSIONAL SUMMARY")
        resume.append("-" * 80)
        summary_ai = self.ai_generate_summary(data['education'], data['skills'], data['experience'])
        resume.append(summary_ai)
        resume.append("")

        # add skills section
        resume.append("CORE COMPETENCIES")
        resume.append("-" * 80)
        skills_text = self.format_skills(data['skills'])
        resume.append(skills_text)
        resume.append("")

        # AI-generated work experience
        resume.append("PROFESSIONAL EXPERIENCE")
        resume.append("-" * 80)
        exp_with_ai = self.ai_generate_full_experience(
            data['experience'], data['skills'], data['education']
        )
        resume.append(exp_with_ai)
        resume.append("")

        # education at the end
        resume.append("EDUCATION")
        resume.append("-" * 80)
        edu_text = self.format_education(data['education'])
        resume.append(edu_text)

        result = '\n'.join(resume)
        return result

    def generate_summary(self, education, skills, experience):
        """Create a professional summary based on the person's background"""
        # parse out the skills
        skills_normalized = skills.replace('\n', ',')
        skill_list = []
        for s in skills_normalized.split(','):
            skill = s.strip()
            if skill:
                skill_list.append(skill)

        # grab top 3 skills
        if len(skill_list) >= 3:
            top_skills = ', '.join(skill_list[:3])
        elif skill_list:
            top_skills = ', '.join(skill_list)
        else:
            top_skills = "various technical and professional skills"

        # check if they have work experience
        exp_lines = experience.split('\n')
        non_empty_lines = [line for line in exp_lines if line.strip()]
        has_experience = len(non_empty_lines) > 2

        # write summary based on experience level
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
        """Let AI generate a more creative professional summary"""
        try:
            # get the key skills first
            skills_normalized = skills.replace('\n', ',')
            all_skills = [s.strip() for s in skills_normalized.split(',') if s.strip()]
            skill_list = all_skills[:5]  # just take top 5

            if skill_list:
                skills_text = ', '.join(skill_list)
            else:
                skills_text = "various skills"

            # build a prompt for the AI model
            education_snippet = education[:80] if len(education) > 80 else education
            experience_snippet = experience[:100] if len(experience) > 100 else experience

            prompt = f"""Write a professional resume summary (2-3 sentences) for someone with:
- Education: {education_snippet}
- Skills: {skills_text}
- Experience: {experience_snippet}

The summary should highlight their strengths and career goals."""

            print(f"Generating AI summary...")

            # tokenize the prompt
            inputs = self.ai_tokenizer(prompt, return_tensors="pt", max_length=400, truncation=True)

            # TODO: maybe adjust temperature lower for more consistent results?
            # generate output
            outputs = self.ai_model.generate(
                inputs.input_ids,
                max_length=180,
                min_length=30,
                temperature=0.85,
                do_sample=True,
                top_p=0.90,
                repetition_penalty=1.4,
            )

            # decode the result
            summary = self.ai_tokenizer.decode(outputs[0], skip_special_tokens=True)
            summary = summary.strip()

            print(f"Raw AI summary: {summary}")

            # sometimes AI repeats the prompt, so clean it up
            lower_summary = summary.lower()
            if lower_summary.startswith('write') or lower_summary.startswith('create') or lower_summary.startswith('summary') or lower_summary.startswith('the summary'):
                # try splitting by colon
                if ':' in summary:
                    parts = summary.split(':', 1)
                    summary = parts[1].strip()
                else:
                    # try newline
                    if '\n' in summary:
                        parts = summary.split('\n', 1)
                        summary = parts[1].strip()

            # clean up any leftover instruction text
            summary = summary.replace('Write a professional resume summary', '')
            summary = summary.replace('(2-3 sentences)', '')
            summary = summary.strip()

            # just to be safe, strip again
            if summary:
                summary = summary.strip()

            # make sure it's reasonable length
            summary_length = len(summary)
            if summary_length > 40 and summary_length < 500:
                print(f"✓ AI generated summary: {summary[:100]}...")
                return summary
            else:
                print(f"✗ AI summary too short/long ({summary_length} chars), using template")
        except Exception as e:
            print(f"AI summary generation failed: {str(e)}")

        # if AI fails, fall back to template
        return self.generate_summary(education, skills, experience)

    def ai_generate_full_experience(self, experience, skills, education):
        """Generate experience section with AI help"""
        # handle empty experience
        if not experience.strip():
            return "  • Ready to bring dedication and skills to a new role"

        # split into lines and remove empty ones
        all_lines = experience.split('\n')
        lines = []
        for line in all_lines:
            stripped = line.strip()
            if stripped:
                lines.append(stripped)

        formatted = []
        current_job = None
        line_index = 0

        # go through each line
        while line_index < len(lines):
            current_line = lines[line_index]

            # job titles are usually short lines without bullets
            is_job_title = len(current_line) < 100
            has_bullet = current_line.startswith('•') or current_line.startswith('-') or current_line.startswith('  ')

            if is_job_title and not has_bullet:
                # found a job title
                if len(formatted) > 0:
                    formatted.append("")  # add blank line between jobs

                formatted.append(current_line.upper())
                current_job = current_line

                # now generate AI content for this job
                print(f"\nGenerating AI content for: {current_job}")
                responsibilities = self.ai_generate_job_responsibilities(current_job, skills, education)

                for resp in responsibilities:
                    formatted.append(resp)

                # skip the old bullet points since we made new ones
                line_index += 1
                while line_index < len(lines):
                    next_line = lines[line_index]
                    has_bullet_next = next_line.startswith('•') or next_line.startswith('-') or next_line.startswith('  ')
                    is_long_line = len(next_line) > 100

                    if has_bullet_next or is_long_line:
                        line_index += 1
                    else:
                        break
                continue

            line_index += 1

        # put it all together
        if formatted:
            result = '\n'.join(formatted)
        else:
            result = self.format_experience(experience, skills)

        print(f"\nGenerated experience section ({len(result)} chars)")
        return result

    def ai_generate_job_responsibilities(self, job_title, skills, education):
        """Use AI to create job bullet points"""
        try:
            # prepare the skills text - keep it short
            if skills and len(skills) > 100:
                skills_text = skills[:100]
            elif skills:
                skills_text = skills
            else:
                skills_text = "various professional skills"

            # make a simple prompt for the model
            prompt = f"""Create 4 professional resume bullet points for a {job_title} position using these skills: {skills_text}

Each bullet point should describe an achievement or responsibility. Be specific and use action verbs."""

            print(f"Generating AI responsibilities for: {job_title}...")

            # tokenize and generate
            tokenized = self.ai_tokenizer(prompt, return_tensors="pt", max_length=400, truncation=True)
            generated = self.ai_model.generate(
                tokenized.input_ids,
                max_length=250,
                min_length=60,
                temperature=0.95,
                do_sample=True,
                top_p=0.92,
                repetition_penalty=1.5,
                no_repeat_ngram_size=2,
                num_return_sequences=1,
            )

            # decode what the AI generated
            ai_text = self.ai_tokenizer.decode(generated[0], skip_special_tokens=True)
            ai_text = ai_text.strip()

            print(f"Raw AI output: {ai_text[:200]}...")

            # clean up the output - sometimes it includes the prompt
            split_lines = ai_text.split('\n')
            good_lines = []

            for ln in split_lines:
                ln = ln.strip()

                # skip prompt repetition
                skip_words = ['create', 'bullet point', 'resume', 'should describe', 'each bullet']
                should_skip = False
                for word in skip_words:
                    if word in ln.lower():
                        should_skip = True
                        break

                if should_skip:
                    continue

                # remove markers like bullets, numbers, etc
                ln = ln.lstrip('•')
                ln = ln.lstrip('-')
                ln = ln.lstrip('*')
                ln = ln.lstrip('1234567890. ')

                # keep if it looks good
                if len(ln) > 15 and len(ln) < 300:
                    good_lines.append(ln)

            # turn into bullet format
            bullet_list = []
            for line in good_lines:
                bullet_list.append(f"  • {line}")

            # if not enough bullets, try splitting differently
            if len(bullet_list) < 2:
                # split by periods
                modified_text = ai_text.replace('. ', '.|')
                parts = modified_text.split('|')
                bullet_list = []

                for part in parts:
                    cleaned = part.strip()
                    cleaned = cleaned.strip('.')

                    # check if it's valid content
                    bad_words = ['create', 'bullet', 'write', 'describe']
                    is_bad = False
                    for bad in bad_words:
                        if bad in cleaned.lower():
                            is_bad = True
                            break

                    if not is_bad and len(cleaned) > 20 and len(cleaned) < 250:
                        bullet_list.append(f"  • {cleaned}")

            # check if we got good results
            if len(bullet_list) >= 2:
                print(f"✓ AI generated {len(bullet_list)} creative bullets!")
                # return max 4 bullets
                return bullet_list[:4]
            else:
                print(f"✗ AI output didn't produce valid bullets, using template")
                # debug: print the raw output to see what went wrong
                # print(f"DEBUG: {ai_text}")

        except Exception as e:
            print(f"AI generation error: {str(e)}")


        # fallback to template
        return self.generate_template_responsibilities(job_title, skills)

    def generate_template_responsibilities(self, job_title, skills):
        """Make some reasonable bullet points based on job title"""
        # figure out what kind of job this is
        if job_title:
            job_lower = job_title.lower()
        else:
            job_lower = ""

        # parse skills if available
        skill_list = []
        if skills:
            for s in skills.split(',')[:3]:
                skill_list.append(s.strip())

        # use job title as seed so same title gives same bullets
        random.seed(hash(job_title))
        bullets = []

        # check what kind of role this is and pick appropriate bullets
        if 'developer' in job_lower or 'engineer' in job_lower or 'programmer' in job_lower or 'software' in job_lower:
            dev_options = [
                "  • Developed and maintained software applications using modern technologies and frameworks",
                "  • Designed and implemented scalable solutions to meet business requirements",
                "  • Collaborated with cross-functional teams to deliver projects on schedule",
                "  • Participated in code reviews and maintained high code quality standards",
                "  • Optimized database queries and improved application performance by 30%",
                "  • Implemented best practices for code quality, testing, and documentation",
            ]
            sample_size = min(4, len(dev_options))
            bullets.extend(random.sample(dev_options, sample_size))


        elif 'manager' in job_lower or 'lead' in job_lower or 'supervisor' in job_lower or 'director' in job_lower:
            mgmt_options = [
                "  • Led team initiatives and coordinated project deliverables across departments",
                "  • Managed cross-functional teams to achieve strategic objectives",
                "  • Improved team efficiency through process optimization and automation",
                "  • Developed and executed strategic plans aligned with company goals",
                "  • Mentored team members and fostered professional development",
                "  • Built and maintained relationships with key stakeholders and clients",
            ]
            sample_size = min(4, len(mgmt_options))
            bullets.extend(random.sample(mgmt_options, sample_size))

        elif 'analyst' in job_lower or 'data' in job_lower or 'research' in job_lower:
            analyst_options = [
                "  • Analyzed complex data sets to drive business insights and recommendations",
                "  • Created comprehensive reports and visualizations for stakeholders",
                "  • Identified trends and opportunities for operational improvements",
                "  • Collaborated with business units to define metrics and reporting requirements",
                "  • Automated reporting processes to improve efficiency and accuracy",
                "  • Maintained data quality and integrity across multiple systems",
            ]
            sample_size = min(4, len(analyst_options))
            bullets.extend(random.sample(analyst_options, sample_size))

        elif 'designer' in job_lower or 'creative' in job_lower or 'ui' in job_lower or 'ux' in job_lower:
            design_options = [
                "  • Created user-centered designs that improved engagement and satisfaction",
                "  • Collaborated with stakeholders to understand requirements and objectives",
                "  • Maintained brand consistency across all deliverables and touchpoints",
                "  • Produced wireframes, mockups, and prototypes for new features",
                "  • Conducted user research and usability testing to inform design decisions",
                "  • Managed multiple design projects with competing deadlines",
            ]
            sample_size = min(4, len(design_options))
            bullets.extend(random.sample(design_options, sample_size))

        else:
            # generic bullets for other roles
            generic_options = [
                "  • Contributed to team objectives and organizational goals",
                "  • Demonstrated strong problem-solving and analytical skills",
                "  • Collaborated effectively with colleagues and stakeholders",
                "  • Managed multiple priorities in fast-paced environment",
                "  • Maintained excellent communication with internal and external partners",
                "  • Provided excellent customer service and support",
            ]
            sample_size = min(4, len(generic_options))
            bullets.extend(random.sample(generic_options, sample_size))

        # add a skill-specific bullet if we have room
        if skill_list and len(bullets) < 4:
            first_two = skill_list[:2]
            skill_text = ', '.join(first_two)
            bullets.insert(0, f"  • Utilized {skill_text} to deliver high-quality results")

        # reset random seed
        random.seed()

        # return max 4 bullets
        return bullets[:4]

    def format_skills(self, skills):
        """Format the skills section nicely"""
        if not skills:
            return "• To be added based on role requirements"

        # normalize line breaks to commas
        normalized = skills.replace('\n', ',')
        skill_list = []
        for s in normalized.split(','):
            cleaned = s.strip()
            if cleaned:
                skill_list.append(cleaned)

        # separate into technical and soft skills
        technical = []
        soft = []
        soft_keywords = ['communication', 'leadership', 'teamwork', 'management',
                        'problem-solving', 'analytical', 'creative', 'collaboration']

        for skill in skill_list:
            skill_lower = skill.lower()
            is_soft = False

            for keyword in soft_keywords:
                if keyword in skill_lower:
                    is_soft = True
                    break

            if is_soft:
                soft.append(skill)
            else:
                technical.append(skill)

        # build the result string
        result = ""
        if technical:
            result += "Technical Skills: " + ", ".join(technical)
            if soft:
                result += "\n"
        if soft:
            result += "Professional Skills: " + ", ".join(soft)

        # if we couldn't categorize anything, just list them
        if not result:
            lines = []
            for skill in skill_list:
                lines.append("• " + skill)
            result = "\n".join(lines)

        return result

    def format_experience(self, experience, skills=""):
        """Format the experience section"""
        if not experience:
            return "• Ready to bring dedication and skills to a new role"

        # split into lines and clean up
        all_lines = experience.split('\n')
        lines = []
        for line in all_lines:
            cleaned = line.strip()
            if cleaned:
                lines.append(cleaned)

        formatted = []
        for line in lines:
            # job titles are usually short and don't have bullets
            is_short = len(line) < 100
            has_bullet = line.startswith('•') or line.startswith('-')

            if is_short and not has_bullet:
                # this is probably a job title or company
                if formatted:
                    formatted.append("\n" + line.upper())
                else:
                    formatted.append(line.upper())
            else:
                # this is a description or bullet point
                if not has_bullet:
                    formatted.append("  • " + line)
                else:
                    formatted.append("  " + line)

        return '\n'.join(formatted)

    def format_education(self, education):
        """Format the education section"""
        if not education:
            return "• Educational background to be provided"

        # split and clean lines
        all_lines = education.split('\n')
        lines = []
        for line in all_lines:
            cleaned = line.strip()
            if cleaned:
                lines.append(cleaned)

        formatted = []
        for line in lines:
            # add bullet if not already there
            if not line.startswith('•') and not line.startswith('-'):
                formatted.append("• " + line)
            else:
                formatted.append(line)

        return '\n'.join(formatted)

