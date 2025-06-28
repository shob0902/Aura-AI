# AURA AI - Personal AI Assistant with Resume Analysis

An AI assistant that can analyze your resume and answer questions about your background, experience, skills, and more. Built with Python, OpenAI GPT, and speech recognition.

## Features

📄 **Resume Analysis**: Upload your resume and ask questions about your background
🎯 **Smart Responses**: AI analyzes your resume content to provide personalized answers
⏰ **General Assistance**: Get time, open websites, and general chat
🔧 **Cross-Platform**: Works on Windows, macOS, and Linux

## Setup Instructions

### 1. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key

1. Get your OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Open `config.py` and replace `"your-openai-api-key-here"` with your actual API key

### 3. Add Your Resume

Place your resume file in the project directory with one of these names:
- `resume.pdf` (recommended)
- `resume.docx`
- `resume.txt`

The AI will automatically load and analyze your resume when you start the application.

## Usage

### Starting the AI Assistant

```bash
python main.py
```

#### Resume Analysis
- **"What's my background in Python?"** - Ask about specific skills
- **"Tell me about my work experience"** - Get work history summary
- **"What are my skills?"** - List your technical skills
- **"What's my education background?"** - Get education details
- **"My contact information"** - Get your contact details

#### General Commands
- **"What time is it?"** - Get current time and date
- **"Open YouTube"** - Open websites (YouTube, Google, GitHub, LinkedIn, etc.)
- **"Help"** - See all available commands
- **"Goodbye"** - Exit the application

#### Natural Conversation
- Ask any question and the AI will respond based on your resume context
- The AI remembers your background and can provide personalized answers

## Example Conversations

```
You: "What's my background in machine learning?"
AI: "Based on your resume, you have experience with Python, TensorFlow, and scikit-learn. You worked on a recommendation system project at TechCorp where you implemented ML algorithms..."

You: "Tell me about my most recent job"
AI: "According to your resume, your most recent position was Senior Software Engineer at Innovation Labs from 2021-2023, where you led a team of 5 developers..."

You: "What skills should I highlight for a data science role?"
AI: "Based on your resume, you should emphasize your Python programming, statistical analysis, and machine learning experience. You also have strong experience with SQL and data visualization..."
```

## File Structure

```
├── main.py              # Main AI assistant application
├── resume_analyzer.py   # Resume parsing and analysis module
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── resume.pdf         # Your resume file (add this)
```

## Configuration Options

Edit `config.py` to customize:

- **API Key**: Your OpenAI API key
- **Resume Path**: Path to your resume file
- **Voice Settings**: Enable/disable voice output
- **AI Model**: Choose between different OpenAI models
- **Language**: Speech recognition language

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   - Windows: `pip install pyaudio`
   - macOS: `brew install portaudio && pip install pyaudio`
   - Linux: `sudo apt-get install python3-pyaudio`

2. **Speech recognition not working**
   - Check your microphone permissions
   - Ensure you have an internet connection (for Google Speech Recognition)

3. **Resume not loading**
   - Make sure your resume file is named `resume.pdf`, `resume.docx`, or `resume.txt`
   - Check that the file is in the project directory

4. **API key errors**
   - Verify your OpenAI API key is correct
   - Ensure you have sufficient API credits

### Voice Commands Not Working?

- Speak clearly and at a normal pace
- Reduce background noise
- Check microphone settings
- Try saying "help" to see available commands

## Privacy & Security

- Your resume data is processed locally and sent to OpenAI for analysis
- No data is stored permanently on external servers
- The AI only has access to the resume content you provide

## Contributing

Feel free to enhance this project by:
- Adding support for more resume formats
- Implementing additional voice commands
- Improving the resume analysis accuracy
- Adding new features like calendar integration

## License

This project is open source and available under the MIT License.

---

**Enjoy your personalized AI assistant!** 🚀 
