import os
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
from auth import login_required

bp = Blueprint('ai', __name__)

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

@bp.route('/ai', methods=('GET', 'POST'))
@login_required
def assistant():
    if request.method == 'GET':
        return render_template('ai/index.html', active_page='ai')
        
    if request.method == 'POST':
        # Accept JSON explicitly for async Fetch API calls
        data = request.get_json() if request.is_json else request.form
        user_input = data.get('prompt', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Please provide a valid prompt.'}), 400
            
        api_key = os.environ.get('GEMINI_API_KEY', 'REDACTED_API_KEY_SECURE')
        
        if not HAS_GENAI:
            return jsonify({'error': 'The google-generativeai package is missing from the virtual environment. Ensure dependencies are fully installed.'}), 500
            
        if not api_key:
            return jsonify({'error': 'GEMINI_API_KEY environment variable is missing. Set it into your environment to instantly unlock AI features!'}), 500
            
        try:
            genai.configure(api_key=api_key)
            # Use gemini-1.5-flash for very fast textual reasoning
            model = genai.GenerativeModel(
                'gemini-1.5-flash',
                system_instruction="You are 'HackConnect AI', a helpful technical AI integrated directly into a Hackathon Platform. Provide highly concise, robust technical advice to users. Help brainstorm ideas, review software stacks, restructure project pitches, and roadmap sprints."
            )
            
            response = model.generate_content(user_input)
            return jsonify({'response': response.text})
            
        except Exception as e:
            return jsonify({'error': f"Internal AI API Error: {str(e)}"}), 500
