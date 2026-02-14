"""
Sample Resume Generator
Creates a sample PDF with multiple resumes for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

def create_sample_resumes(output_path="sample_resumes.pdf"):
    """Create a sample PDF with multiple resumes"""

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Sample resumes data
    resumes = [
        {
            "name": "John Smith",
            "email": "john.smith@email.com",
            "experience": 5,
            "skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis", "SQL"],
            "summary": "Experienced ML Engineer with 5 years in developing production ML systems. Strong background in Python, TensorFlow, and data analysis. Led multiple successful projects in predictive modeling."
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.j@email.com",
            "experience": 3,
            "skills": ["JavaScript", "React", "Node.js", "MongoDB", "Frontend Development"],
            "summary": "Frontend Developer with 3 years of experience building responsive web applications. Expert in React and modern JavaScript. Passionate about creating excellent user experiences."
        },
        {
            "name": "Michael Chen",
            "email": "m.chen@email.com",
            "experience": 7,
            "skills": ["Python", "Django", "FastAPI", "PostgreSQL", "Docker", "AWS"],
            "summary": "Senior Backend Engineer with 7 years of experience in building scalable APIs and microservices. Specialized in Python frameworks, cloud infrastructure, and system architecture."
        },
        {
            "name": "Emily Rodriguez",
            "email": "emily.r@email.com",
            "experience": 4,
            "skills": ["Java", "Spring Boot", "Kubernetes", "CI/CD", "Jenkins"],
            "summary": "DevOps Engineer with 4 years experience in automation and infrastructure. Skilled in container orchestration, CI/CD pipelines, and cloud platforms. Strong Java and Spring background."
        },
        {
            "name": "David Kim",
            "email": "david.kim@email.com",
            "experience": 6,
            "skills": ["Python", "Data Science", "Pandas", "NumPy", "Visualization"],
            "summary": "Data Scientist with 6 years of experience analyzing complex datasets and building predictive models. Expert in Python data stack including Pandas, NumPy, and various visualization tools."
        },
    ]

    for resume in resumes:
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawString(1*inch, height - 1*inch, resume["name"])

        # Contact
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 1.3*inch, resume["email"])

        # Experience
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height - 1.8*inch, "EXPERIENCE")
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 2.1*inch, f"{resume['experience']} years of professional experience")

        # Skills
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height - 2.6*inch, "TECHNICAL SKILLS")
        c.setFont("Helvetica", 12)
        skills_text = ", ".join(resume["skills"])
        c.drawString(1*inch, height - 2.9*inch, skills_text)

        # Summary
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height - 3.4*inch, "PROFESSIONAL SUMMARY")
        c.setFont("Helvetica", 11)

        # Wrap text
        summary_lines = []
        words = resume["summary"].split()
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if c.stringWidth(test_line, "Helvetica", 11) < 6.5*inch:
                current_line = test_line
            else:
                summary_lines.append(current_line)
                current_line = word
        if current_line:
            summary_lines.append(current_line)

        y_position = height - 3.7*inch
        for line in summary_lines:
            c.drawString(1*inch, y_position, line)
            y_position -= 0.2*inch

        # Work History (dummy)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height - 5*inch, "WORK HISTORY")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, height - 5.3*inch, "Senior Developer - Tech Corp")
        c.setFont("Helvetica", 11)
        c.drawString(1*inch, height - 5.6*inch, "2020 - Present")
        c.drawString(1*inch, height - 5.9*inch, "• Led development of key features")
        c.drawString(1*inch, height - 6.2*inch, "• Mentored junior developers")
        c.drawString(1*inch, height - 6.5*inch, "• Improved system performance by 40%")

        # Education
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height - 7.2*inch, "EDUCATION")
        c.setFont("Helvetica", 11)
        c.drawString(1*inch, height - 7.5*inch, "Bachelor of Science in Computer Science")
        c.drawString(1*inch, height - 7.8*inch, "University of Technology, 2015")

        # Start new page for next resume
        c.showPage()

    c.save()
    print(f"Sample resume PDF created: {output_path}")
    print(f"Contains {len(resumes)} sample resumes")

if __name__ == "__main__":
    create_sample_resumes()
