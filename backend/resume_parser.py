import fitz  # PyMuPDF
import re
import os
from typing import List, Dict, Optional
from models import Resume


class ResumeParser:
    def __init__(self, upload_dir: str, resume_dir: str):
        self.upload_dir = upload_dir
        self.resume_dir = resume_dir
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(resume_dir, exist_ok=True)

    def extract_resumes_from_pdf(self, pdf_path: str) -> List[Resume]:
        """Extract individual resumes from a multi-page PDF"""
        resumes = []

        try:
            doc = fitz.open(pdf_path)

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()

                # Save individual resume page as separate PDF
                resume_filename = f"resume_page_{page_num + 1}.pdf"
                resume_path = os.path.join(self.resume_dir, resume_filename)

                # Create single page PDF
                single_page_doc = fitz.open()
                single_page_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                single_page_doc.save(resume_path)
                single_page_doc.close()

                # Parse the resume content
                resume_data = self.parse_resume_text(text, resume_path)
                if resume_data:
                    resumes.append(resume_data)

            doc.close()

        except Exception as e:
            print(f"Error extracting resumes: {e}")
            raise

        return resumes

    def parse_resume_text(self, text: str, cv_path: str) -> Optional[Resume]:
        """Parse resume text and extract structured information"""

        if not text or len(text.strip()) < 50:  # Skip empty or too short pages
            return None

        # Extract name (usually at the top, all caps or title case)
        name = self.extract_name(text)

        # Extract email
        email = self.extract_email(text)

        # Extract skills
        skills = self.extract_skills(text)

        # Extract experience (in years)
        experience = self.extract_experience(text)

        return Resume(
            name=name,
            email=email,
            skills=skills,
            experience=experience,
            cv_path=cv_path,
            text_content=text
        )

    def extract_name(self, text: str) -> str:
        """Extract candidate name from resume text"""
        lines = text.split('\n')

        # Usually name is in first few lines
        for line in lines[:5]:
            line = line.strip()
            # Look for lines that are likely names (2-4 words, capitalized)
            if line and len(line.split()) <= 4 and line[0].isupper():
                # Avoid common headers
                if not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum', 'vitae', 'page']):
                    return line

        return "Unknown"

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)

        if matches:
            return matches[0]

        return None

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""

        # Common tech skills to look for
        common_skills = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Ruby', 'PHP', 'Go', 'Rust',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring', 'Express',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'Oracle',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'CI/CD',
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision',
            'Data Analysis', 'Data Science', 'Pandas', 'NumPy', 'Scikit-learn',
            'HTML', 'CSS', 'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum',
            'Linux', 'Windows', 'MacOS', 'Bash', 'Shell Scripting',
            'Frontend Development', 'Backend Development', 'Full Stack',
            'UI/UX', 'Testing', 'QA', 'Selenium', 'Jest', 'Pytest'
        ]

        found_skills = []
        text_lower = text.lower()

        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)

        return found_skills

    def extract_experience(self, text: str) -> Optional[int]:
        """Extract years of experience from resume text"""

        # Look for patterns like "5 years", "5+ years", "5 yrs"
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return int(matches[0])

        return None
