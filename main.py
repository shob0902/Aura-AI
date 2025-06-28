import os
import webbrowser
import google.generativeai as genai
from config import GEMINI_API_KEY, RESUME_FILE_PATH, MODEL_NAME, TEMPERATURE, MAX_TOKENS
import datetime
import random
import numpy as np
from resume_analyzer import ResumeAnalyzer
import json
import sys

class PersonalAIAgent:
    def __init__(self):
        self.chat_history = []
        self.resume_analyzer = ResumeAnalyzer(RESUME_FILE_PATH)
        self.resume_loaded = False
        self.resume_context = ""
        self.sample_resume_text = ""
        self.shobhit_resume_data = ""
        
        # Initialize Google Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)
        
        # Load resume and sample resume
        self.load_resume()
        self.load_sample_resume()
        self.load_shobhit_resume_data()
    
    def load_resume(self):
        """Load and analyze the user's resume"""
        print("Loading your resume...")
        if self.resume_analyzer.load_resume():
            self.resume_loaded = True
            self.resume_context = self.resume_analyzer.get_resume_text()
            print("✅ Your resume loaded successfully!")
            print(self.resume_analyzer.get_resume_summary())
        else:
            print("⚠️  Your resume not found. The AI will still work with the sample resume.")
    
    def load_sample_resume(self):
        """Load the sample resume text"""
        try:
            with open("sample_resume.txt", "r", encoding="utf-8") as file:
                self.sample_resume_text = file.read()
            print("✅ Sample resume loaded successfully!")
        except Exception as e:
            print(f"⚠️  Could not load sample resume: {e}")
    
    def load_shobhit_resume_data(self):
        """Load Shobhit's comprehensive resume data"""
        try:
            with open("shobhit_resume_data.txt", "r", encoding="utf-8") as file:
                self.shobhit_resume_data = file.read()
            print("✅ Shobhit's comprehensive resume data loaded successfully!")
        except Exception as e:
            print(f"⚠️  Could not load Shobhit's resume data: {e}")
    
    def print_response(self, text):
        """Print AI response with formatting"""
        print(f"\n🤖 AI: {text}")
        print("\n" + "="*50 + "\n")
    
    def get_user_input(self):
        """Get text input from user"""
        try:
            query = input("👤 You: ").strip()
            return query.lower() if query else ""
        except KeyboardInterrupt:
            return "exit"
        except EOFError:
            return "exit"
    
    def analyze_resume_question(self, question):
        """Analyze resume-specific questions using AI"""
        if not self.resume_loaded and not self.sample_resume_text and not self.shobhit_resume_data:
            return "I don't have access to any resume data. Please add your resume file to the project directory."
        
        # Create a comprehensive prompt for resume analysis
        resume_data = ""
        if self.shobhit_resume_data:
            resume_data += f"SHOBHIT'S COMPREHENSIVE RESUME:\n{self.shobhit_resume_data}\n\n"
        
        if self.resume_loaded:
            resume_data += f"USER'S RESUME (PDF):\n{self.resume_context}\n\n"
        
        if self.sample_resume_text:
            resume_data += f"SAMPLE RESUME FOR COMPARISON:\n{self.sample_resume_text}\n\n"
        
        prompt = f"""
You are a personal AI assistant analyzing Shobhit Shourya's resume and related information. Here is the comprehensive resume data:

{resume_data}

Based on this resume information, please answer the following question: {question}

Provide a detailed, helpful response that draws from the resume information. If the information isn't available in the resume, say so clearly.

Focus on Shobhit's background, skills, experience, projects, and achievements. Be specific and provide concrete examples from his resume.

Response:"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error analyzing resume: {e}"
    
    def chat_with_ai(self, query):
        """General chat with AI"""
        # Add context about the user if resume is loaded
        context = ""
        if self.shobhit_resume_data:
            context += f"\n\nShobhit's Resume Context: Available (comprehensive data loaded)"
        
        if self.resume_loaded:
            context += f"\n\nUser's Resume Context: {self.resume_analyzer.get_resume_summary()}"
        
        if self.sample_resume_text:
            context += f"\n\nSample Resume Available: Yes (for comparison and reference)"
        
        try:
            full_prompt = f"You are a helpful personal AI assistant for Shobhit Shourya. You have access to comprehensive resume information.{context}\n\nUser question: {query}"
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error in AI chat: {e}"
    
    def get_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%B %d, %Y")
        return f"The current time is {time_str} on {date_str}"
    
    def open_website(self, site_name):
        """Open websites"""
        sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "linkedin": "https://linkedin.com",
            "stackoverflow": "https://stackoverflow.com",
            "wikipedia": "https://wikipedia.org"
        }
        
        if site_name in sites:
            webbrowser.open(sites[site_name])
            return f"Opening {site_name}..."
        else:
            return f"Sorry, I don't know how to open {site_name}"
    
    def get_resume_info(self, info_type):
        """Get specific resume information"""
        if not self.shobhit_resume_data:
            return "Shobhit's resume data not loaded. Please check the file."
        
        # Parse the comprehensive resume data for specific information
        if info_type == "contact":
            return "Name: Shobhit Shourya\nEmail: shouryashobhit1@gmail.com\nPhone: +91 7477012992"
        elif info_type == "education":
            return """• Bachelor of Technology (B.Tech) at Vellore Institute of Technology (VIT), Vellore, India (2022 – Present)
• Class 12 (CBSE), Delhi Public School, Bhopal, India, 2022 — 82%
• Class 10 (CBSE), Delhi Public School, Bhopal, India, 2020 — 87%"""
        elif info_type == "experience":
            return """• Microsoft Azure AI Fundamentals (AI-900) – Internship at Microsoft (May – June 2024)
• Deloitte Australia – Data Analytics Job Simulation (June 2025)
• AWS APAC – Solutions Architecture Virtual Experience (March 2025)"""
        elif info_type == "skills":
            return """Languages & Programming: Java, JavaScript, TypeScript, SQL
Frontend Development: HTML5, CSS3, React.js
Design & Prototyping: Figma
App Development: Android Studio, Expo
Cloud & DevOps: AWS (Elastic Beanstalk, Architecture Diagramming, Pricing Models)
Data & Analysis: Tableau, Excel, Spreadsheets, Data Modeling, Data Analysis"""
        else:
            return "Please specify what information you want: contact, education, experience, or skills"
    
    def compare_resumes(self):
        """Compare user's resume with sample resume"""
        if not self.shobhit_resume_data or not self.sample_resume_text:
            return "I need both Shobhit's resume and the sample resume to make a comparison."
        
        prompt = f"""
You are an expert resume analyst. Please compare these two resumes and provide insights:

SHOBHIT'S RESUME:
{self.shobhit_resume_data}

SAMPLE RESUME:
{self.sample_resume_text}

Please provide a detailed comparison including:
1. Strengths and weaknesses of each resume
2. Key differences in structure, content, and presentation
3. Suggestions for improvement for Shobhit's resume
4. Which resume is stronger and why
5. Specific recommendations for Shobhit's resume

Response:"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error comparing resumes: {e}"
    
    def process_command(self, query):
        """Process user commands"""
        query_lower = query.lower()
        
        # Resume analysis commands
        if any(keyword in query_lower for keyword in ["resume", "cv", "about me", "my background", "my experience", "shobhit", "skills"]):
            return self.analyze_resume_question(query)
        
        # Resume comparison command
        if any(keyword in query_lower for keyword in ["compare", "comparison", "vs", "versus"]):
            return self.compare_resumes()
        
        # Time commands
        if any(keyword in query_lower for keyword in ["time", "what time", "current time"]):
            return self.get_time()
        
        # Website opening commands
        for site in ["youtube", "google", "github", "linkedin", "stackoverflow", "wikipedia"]:
            if f"open {site}" in query_lower:
                return self.open_website(site)
        
        # Resume information commands
        if "my contact" in query_lower or "my email" in query_lower or "my phone" in query_lower:
            return self.get_resume_info("contact")
        elif "my education" in query_lower or "my degree" in query_lower:
            return self.get_resume_info("education")
        elif "my experience" in query_lower or "my work" in query_lower:
            return self.get_resume_info("experience")
        elif "my skills" in query_lower or "my technologies" in query_lower:
            return self.get_resume_info("skills")
        
        # Exit commands
        if any(keyword in query_lower for keyword in ["quit", "exit", "stop", "goodbye", "bye"]):
            return "EXIT"
        
        # Help command
        if "help" in query_lower or "what can you do" in query_lower:
            return """I can help you with:

📄 Resume Analysis:
- Ask questions about Shobhit's resume, experience, education, skills
- "What are Shobhit's skills?"
- "Tell me about Shobhit's work experience"
- "What projects has Shobhit worked on?"
- "What's Shobhit's background in Java?"

🔄 Resume Comparison:
- "Compare Shobhit's resume with the sample"
- "How does Shobhit's resume compare to the sample?"
- "What are the differences between the resumes?"

⏰ General Assistance:
- "What time is it?"
- "Open YouTube/Google/GitHub/LinkedIn"

💬 General Chat:
- Ask me anything and I'll respond based on Shobhit's resume context

Just type your questions and I'll help you!"""
        
        # Default: general chat
        return self.chat_with_ai(query)
    
    def run(self):
        """Main loop for the AI agent"""
        print("🤖 Hello! I'm your personal AI assistant powered by Google Gemini.")
        print("📄 I can analyze Shobhit's resume and compare it with the sample resume.")
        print("💡 Type 'help' to see what I can do, or just ask me anything!")
        print("="*50)
        
        while True:
            query = self.get_user_input()
            
            if not query:
                continue
            
            if query == "exit":
                print("👋 Goodbye! Have a great day!")
                break
            
            response = self.process_command(query)
            
            if response == "EXIT":
                print("👋 Goodbye! Have a great day!")
                break
            
            self.print_response(response)

if __name__ == '__main__':
    # Check if API key is configured
    if GEMINI_API_KEY == "your-gemini-api-key-here":
        print("❌ Please configure your Google Gemini API key in config.py")
        print("1. Get your API key from https://makersuite.google.com/app/apikey")
        print("2. Replace 'your-gemini-api-key-here' in config.py with your actual API key")
        sys.exit(1)
    
    try:
        agent = PersonalAIAgent()
        agent.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your configuration and try again.")