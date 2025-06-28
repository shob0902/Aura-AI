import PyPDF2
import docx
import os
import re
from typing import Dict, List, Optional
import json

class ResumeAnalyzer:
    def __init__(self, resume_path: str = "resume.pdf"):
        self.resume_path = resume_path
        self.resume_text = ""
        self.extracted_info = {}
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF resume"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX resume"""
        try:
            doc = docx.Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    def load_resume(self) -> bool:
        """Load resume from file"""
        if not os.path.exists(self.resume_path):
            print(f"Resume file not found: {self.resume_path}")
            return False
        
        file_extension = os.path.splitext(self.resume_path)[1].lower()
        
        if file_extension == '.pdf':
            self.resume_text = self.extract_text_from_pdf(self.resume_path)
        elif file_extension == '.docx':
            self.resume_text = self.extract_text_from_docx(self.resume_path)
        elif file_extension == '.txt':
            with open(self.resume_path, 'r', encoding='utf-8') as file:
                self.resume_text = file.read()
        else:
            print(f"Unsupported file format: {file_extension}")
            return False
        
        if self.resume_text.strip():
            self.extract_structured_info()
            return True
        return False
    
    def extract_structured_info(self):
        """Extract structured information from resume text"""
        self.extracted_info = {
            'name': self.extract_name(),
            'email': self.extract_email(),
            'phone': self.extract_phone(),
            'education': self.extract_education(),
            'experience': self.extract_experience(),
            'skills': self.extract_skills(),
            'projects': self.extract_projects(),
            'certifications': self.extract_certifications()
        }
    
    def extract_name(self) -> str:
        """Extract name from resume"""
        # Simple pattern matching for name extraction
        lines = self.resume_text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if len(line) > 2 and len(line) < 50:
                # Look for patterns that might be names
                if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', line):
                    return line
        return "Name not found"
    
    def extract_email(self) -> str:
        """Extract email from resume"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.resume_text)
        return emails[0] if emails else "Email not found"
    
    def extract_phone(self) -> str:
        """Extract phone number from resume"""
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, self.resume_text)
        return phones[0] if phones else "Phone not found"
    
    def extract_education(self) -> List[Dict]:
        """Extract education information"""
        education = []
        lines = self.resume_text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['bachelor', 'master', 'phd', 'degree', 'university', 'college']):
                edu_entry = {
                    'degree': line.strip(),
                    'institution': lines[i-1].strip() if i > 0 else "Not specified",
                    'year': self.extract_year_from_text(line)
                }
                education.append(edu_entry)
        
        return education
    
    def extract_experience(self) -> List[Dict]:
        """Extract work experience"""
        experience = []
        lines = self.resume_text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['experience', 'work', 'job', 'position', 'role']):
                exp_entry = {
                    'title': line.strip(),
                    'company': lines[i-1].strip() if i > 0 else "Not specified",
                    'duration': self.extract_duration_from_text(line)
                }
                experience.append(exp_entry)
        
        return experience
    
    def extract_skills(self) -> List[str]:
        """Extract skills from resume"""
        skills = []
        lines = self.resume_text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if 'skills' in line_lower or 'technologies' in line_lower:
                # Extract skills from the same line or next few lines
                skill_text = line
                for i in range(1, 5):  # Check next 5 lines
                    if i < len(lines):
                        skill_text += " " + lines[i]
                
                # Extract individual skills
                skill_pattern = r'\b[A-Za-z+#]+(?:\s*[A-Za-z+#]+)*\b'
                found_skills = re.findall(skill_pattern, skill_text)
                skills.extend([s.strip() for s in found_skills if len(s.strip()) > 2])
                break
        
        return list(set(skills))  # Remove duplicates
    
    def extract_projects(self) -> List[Dict]:
        """Extract project information"""
        projects = []
        lines = self.resume_text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if 'project' in line_lower:
                project_entry = {
                    'name': line.strip(),
                    'description': lines[i+1].strip() if i+1 < len(lines) else "No description"
                }
                projects.append(project_entry)
        
        return projects
    
    def extract_certifications(self) -> List[str]:
        """Extract certifications"""
        certifications = []
        lines = self.resume_text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if 'certification' in line_lower or 'certified' in line_lower:
                certifications.append(line.strip())
        
        return certifications
    
    def extract_year_from_text(self, text: str) -> str:
        """Extract year from text"""
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)
        return years[0] if years else "Year not specified"
    
    def extract_duration_from_text(self, text: str) -> str:
        """Extract duration from text"""
        duration_pattern = r'\b\d{4}\s*[-–]\s*\d{4}|\b\d{4}\s*[-–]\s*present|\b\d{4}\s*[-–]\s*now\b'
        durations = re.findall(duration_pattern, text, re.IGNORECASE)
        return durations[0] if durations else "Duration not specified"
    
    def get_resume_summary(self) -> str:
        """Get a summary of the resume"""
        summary = f"""
Resume Summary for {self.extracted_info.get('name', 'Unknown')}:

Contact Information:
- Email: {self.extracted_info.get('email', 'Not found')}
- Phone: {self.extracted_info.get('phone', 'Not found')}

Education: {len(self.extracted_info.get('education', []))} entries
Experience: {len(self.extracted_info.get('experience', []))} entries
Skills: {len(self.extracted_info.get('skills', []))} skills identified
Projects: {len(self.extracted_info.get('projects', []))} projects
Certifications: {len(self.extracted_info.get('certifications', []))} certifications
        """
        return summary.strip()
    
    def save_extracted_info(self, filename: str = "resume_data.json"):
        """Save extracted information to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_info, f, indent=2, ensure_ascii=False)
    
    def get_resume_text(self) -> str:
        """Get the raw resume text"""
        return self.resume_text 