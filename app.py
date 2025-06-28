from flask import Flask, render_template, request, jsonify, session
from main import PersonalAIAgent
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Initialize the AI assistant
ai_assistant = PersonalAIAgent()

@app.route('/')
def home():
    """Main portfolio page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/projects')
def projects():
    """Projects page"""
    return render_template('projects.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from AI assistant
        response = ai_assistant.analyze_resume_question(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing message: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/resume-info')
def get_resume_info():
    """Get resume information for the frontend"""
    try:
        info = {
            'contact': ai_assistant.get_resume_info('contact'),
            'education': ai_assistant.get_resume_info('education'),
            'experience': ai_assistant.get_resume_info('experience'),
            'skills': ai_assistant.get_resume_info('skills')
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 