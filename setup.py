#!/usr/bin/env python3
"""
Setup script for Personal AI Assistant
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("Try installing manually: pip install -r requirements.txt")
        return False
    return True

def create_config():
    """Create config file if it doesn't exist"""
    if not os.path.exists("config.py"):
        print("📝 Creating config.py...")
        config_content = '''# OpenAI API Configuration
apikey = "your-openai-api-key-here"  # Replace with your actual OpenAI API key

# Resume Analysis Configuration
RESUME_FILE_PATH = "resume.pdf"  # Path to your resume file
RESUME_TEXT_FILE = "resume_text.txt"  # Extracted text from resume

# Voice Configuration
VOICE_ENABLED = True
LANGUAGE = "en-in"

# AI Model Configuration
MODEL_NAME = "gpt-3.5-turbo"  # Updated to use chat completion model
TEMPERATURE = 0.7
MAX_TOKENS = 1000
'''
        with open("config.py", "w") as f:
            f.write(config_content)
        print("✅ config.py created")
        print("⚠️  Remember to add your OpenAI API key to config.py")

def check_resume_file():
    """Check if resume file exists"""
    resume_files = ["resume.pdf", "resume.docx", "resume.txt"]
    for file in resume_files:
        if os.path.exists(file):
            print(f"✅ Resume file found: {file}")
            return True
    
    print("⚠️  No resume file found")
    print("Please add your resume as one of these files:")
    for file in resume_files:
        print(f"   - {file}")
    return False

def main():
    """Main setup function"""
    print("🚀 Setting up Personal AI Assistant...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create config file
    create_config()
    
    # Check for resume file
    check_resume_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Add your OpenAI API key to config.py")
    print("2. Add your resume file (resume.pdf, resume.docx, or resume.txt)")
    print("3. Run: python main.py")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main() 