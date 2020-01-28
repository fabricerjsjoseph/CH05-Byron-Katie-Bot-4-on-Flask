

# import open source modules

import glob
import re

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

# Initialise list to store user inputs
user_message_log=[]

# Initialise list to store chatbot responses
all_bot_responses_list=[]


def gen_all_bot_responses(first_message):

    # Generate the 4 questions based on the user's 1st message
    for question_no in range(4):
        response='LUCY: ' + four_questions_list[question_no]+' {}?'.format(first_message)
        all_bot_responses_list.append(response)

    # Display the 3 statements of the turnaround sections
    tr_statement_1='LUCY: '+ turnarounds_list[0]+' {}'.format(first_message)+'... type OK to continue.'
    tr_statement_2='LUCY: '+ turnarounds_list[1]+' type OK to continue.'
    tr_statement_3='LUCY: '+ turnarounds_list[2]+'.. type OK to continue.'
    all_bot_responses_list.extend([tr_statement_1,tr_statement_2,tr_statement_3])

    # Generate the three turnaround questions based on the user's 1st message
    turnaround_one='LUCY: ' + turnarounds_list[3]+' {}'.format(turnaround_one_generator(first_message))
    turnaround_two='LUCY: ' + turnarounds_list[4]+' {}'.format(turnaround_two_generator(first_message))
    turnaround_three='LUCY: ' + turnarounds_list[5]+' {}'.format(turnaround_three_generator(first_message))

    all_bot_responses_list.extend([turnaround_one,turnaround_two,turnaround_three])

    # Add Closing Statement
    closing_statement=statements_list[1]+' {}'.format(first_message)
    all_bot_responses_list.append(closing_statement)


    return all_bot_responses_list

def bot_response(user_message):

    # Add user's message to list
    user_message_log.append(user_message)

    # Calculate no of user messages stored in list
    no_messages=len(user_message_log)

    # Only run bot_response function once
    if no_messages==1:
        # Generate all bot reponses based on 1st user message
        gen_all_bot_responses(user_message_log[0])


    # Add bot message to conversation list
    response= all_bot_responses_list[no_messages-1]

    return response



from flask import Flask, render_template, request

# Create the App Object
app = Flask(__name__)

# Change Flask environment from Production to Development
#get_ipython().run_line_magic('env', 'FLASK_ENV=development')


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    user_message = request.args.get('msg')
    return str(bot_response(user_message))



# import webbrowser module
import webbrowser

# Register webbrowser
chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))


if __name__ == "__main__":
    webbrowser.get('chrome').open_new('http://127.0.0.1:5000/')
    app.run(debug=False)
