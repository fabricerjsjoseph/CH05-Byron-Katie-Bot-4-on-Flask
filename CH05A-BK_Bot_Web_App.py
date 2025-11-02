

# import open source modules

import glob
import re
import os

# import private modules

from Turnaround_One import turnaround_one_generator
from Turnaround_Two import turnaround_two_generator
from Turnaround_Three import turnaround_three_generator


# UNPACKING DATA STORED IN TEXT FILES

# Import all text files in working directory
txt_list=glob.glob(r"Txt/*.txt")

# Initialise empty to store data from text files
master_list=[]

# Read each text file and store data in master_list
for txt in txt_list:
    with open(txt,'r',encoding='utf-8') as f:
        data=f.readlines()
        data=[re.sub('\n','',item) for item in data]
        master_list.append(data)

# Store all BOT generated statements such as greetings in list
statements_list=master_list[0]

# Store all questions in list
four_questions_list=master_list[1]

# Store all guidelines to questions in list
four_questions_guidance_list=master_list[2]

# Store all turnaround questions & related messages
turnarounds_list=master_list[3]


def gen_all_bot_responses(first_message):
    """Generate all bot responses for the entire conversation based on the first message."""
    responses = []
    
    # Generate the 4 questions based on the user's 1st message
    for question_no in range(4):
        response='LUCY: ' + four_questions_list[question_no]+' {}?'.format(first_message)
        responses.append(response)

    # Display the 3 statements of the turnaround sections
    if len(turnarounds_list) > 0:
        tr_statement_1='LUCY: '+ turnarounds_list[0]+' {}'.format(first_message)+'... type OK to continue.'
        responses.append(tr_statement_1)
    if len(turnarounds_list) > 1:
        tr_statement_2='LUCY: '+ turnarounds_list[1]+' type OK to continue.'
        responses.append(tr_statement_2)
    if len(turnarounds_list) > 2:
        tr_statement_3='LUCY: '+ turnarounds_list[2]+'.. type OK to continue.'
        responses.append(tr_statement_3)

    try:
        # Generate the three turnaround questions based on the user's 1st message
        if len(turnarounds_list) > 3:
            turnaround_one='LUCY: ' + turnarounds_list[3]+' {}'.format(turnaround_one_generator(first_message))
            responses.append(turnaround_one)
        if len(turnarounds_list) > 4:
            turnaround_two='LUCY: ' + turnarounds_list[4]+' {}'.format(turnaround_two_generator(first_message))
            responses.append(turnaround_two)
        if len(turnarounds_list) > 5:
            turnaround_three='LUCY: ' + turnarounds_list[5]+' {}'.format(turnaround_three_generator(first_message))
            responses.append(turnaround_three)
    except Exception as e:
        # If turnaround generation fails, provide a graceful fallback
        responses.append('LUCY: I had trouble generating turnarounds for this statement. Let\'s continue with your reflections.')
        print(f"Turnaround generation error: {e}")

    # Add Closing Statement
    closing_statement=statements_list[1]+' {}'.format(first_message)
    responses.append(closing_statement)

    return responses

def bot_response(user_message, user_message_log, all_bot_responses_list, use_llm=False):
    """Generate bot response based on user message and conversation state."""
    
    # Validate user message
    if not user_message or not user_message.strip():
        return "LUCY: Please share your thought with me.", user_message_log, all_bot_responses_list
    
    # Add user's message to list
    user_message_log.append(user_message)

    # Calculate no of user messages stored in list
    no_messages=len(user_message_log)

    # Try LLM mode if enabled and available
    if use_llm and config.LLM_ENABLED and llm_client.is_available():
        llm_response = llm_client.generate_byron_katie_response(
            user_message, 
            no_messages - 1, 
            user_message_log
        )
        
        # If LLM generated a response, use it
        if llm_response:
            response = f"LUCY: {llm_response}" if not llm_response.startswith("LUCY:") else llm_response
            return response, user_message_log, all_bot_responses_list

    # Fall back to NLP mode (original behavior)
    # Only run bot_response function once
    if no_messages==1:
        # Generate all bot reponses based on 1st user message
        all_bot_responses_list = gen_all_bot_responses(user_message_log[0])

    # Check if we have responses
    if no_messages > len(all_bot_responses_list):
        response = "LUCY: Thank you for sharing. You've completed the inquiry process. Click 'Start New Session' to begin again."
    else:
        # Add bot message to conversation list
        response = all_bot_responses_list[no_messages-1]

    return response, user_message_log, all_bot_responses_list



from flask import Flask, render_template, request, session, jsonify
import secrets
import config
from llm_client import LLMClient

# Create the App Object
app = Flask(__name__)
# Set secret key for session management
app.secret_key = config.SECRET_KEY or secrets.token_hex(16)

# Initialize LLM client
llm_client = LLMClient()


@app.route("/")
def home():
    """Render the home page."""
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    """Handle bot response with session management."""
    user_message = request.args.get('msg', '').strip()
    
    # Initialize session variables if not present
    if 'user_message_log' not in session:
        session['user_message_log'] = []
    if 'all_bot_responses_list' not in session:
        session['all_bot_responses_list'] = []
    if 'use_llm' not in session:
        session['use_llm'] = config.LLM_ENABLED
    
    # Get current session state
    user_message_log = session['user_message_log']
    all_bot_responses_list = session['all_bot_responses_list']
    use_llm = session.get('use_llm', config.LLM_ENABLED)
    
    # Generate response
    response, user_message_log, all_bot_responses_list = bot_response(
        user_message, user_message_log, all_bot_responses_list, use_llm
    )
    
    # Update session
    session['user_message_log'] = user_message_log
    session['all_bot_responses_list'] = all_bot_responses_list
    
    # Calculate progress
    total_steps = len(all_bot_responses_list) if all_bot_responses_list else 11
    current_step = len(user_message_log)
    
    return jsonify({
        'response': str(response),
        'progress': {
            'current': current_step,
            'total': total_steps
        },
        'mode': 'LLM' if use_llm and config.LLM_ENABLED else 'NLP'
    })

@app.route("/reset")
def reset_session():
    """Reset the conversation session."""
    session.clear()
    return jsonify({'status': 'success', 'message': 'Session reset successfully'})

@app.route("/toggle_mode", methods=['POST'])
def toggle_mode():
    """Toggle between NLP and LLM mode."""
    if not config.LLM_ENABLED or not llm_client.is_available():
        return jsonify({
            'status': 'error',
            'message': 'LLM mode is not available. Please configure LLM_API_URL.',
            'mode': 'NLP'
        })
    
    current_mode = session.get('use_llm', False)
    session['use_llm'] = not current_mode
    
    return jsonify({
        'status': 'success',
        'mode': 'LLM' if session['use_llm'] else 'NLP',
        'message': f"Switched to {'LLM' if session['use_llm'] else 'NLP'} mode"
    })

@app.route("/status")
def get_status():
    """Get current configuration and mode status."""
    return jsonify({
        'llm_enabled': config.LLM_ENABLED,
        'llm_available': llm_client.is_available(),
        'llm_api_url': config.LLM_API_URL if config.LLM_API_URL else 'Not configured',
        'llm_model': config.LLM_MODEL,
        'current_mode': 'LLM' if session.get('use_llm', False) else 'NLP',
        'can_toggle': config.LLM_ENABLED and llm_client.is_available()
    })


if __name__ == "__main__":
    import webbrowser
    import sys
    
    # Cross-platform browser opening
    port = 5000
    url = f'http://127.0.0.1:{port}/'
    
    # Try to open browser (works across platforms)
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print(f"Please open your browser and navigate to: {url}")
    
    # Run the app
    print(f"Starting Lucy - Byron Katie Bot on {url}")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, port=port, use_reloader=False)
