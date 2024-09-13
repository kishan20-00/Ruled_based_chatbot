from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]
marks_collection = db["marks"]

# State to keep track of user interaction
chat_sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data['user_id']
    message = data['message']

    if user_id not in chat_sessions:
        chat_sessions[user_id] = {'step': 1, 'name': None, 'email': None, 'semester': None}

    session = chat_sessions[user_id]

    # Step 1: Ask for Name
    if session['step'] == 1:
        session['name'] = message
        session['step'] = 2
        return jsonify({'response': 'Hi, {}! Please provide your email.'.format(session['name'])})

    # Step 2: Ask for Email
    elif session['step'] == 2:
        session['email'] = message
        session['step'] = 3
        return jsonify({'response': 'Thanks, {}! Now please select your semester from 1-8.'.format(session['email']), 'options': list(range(1, 9))})

    # Step 3: Get Semester
    elif session['step'] == 3:
        try:
            semester = int(message)
            if semester not in range(1, 9):
                return jsonify({'response': 'Invalid semester. Please select a semester from 1 to 8.'})

            session['semester'] = semester
            session['step'] = 4

            # Fetch the result from MongoDB
            results = marks_collection.find_one({'email': session['email'], 'semester': session['semester']})

            if results:
                return jsonify({'response': 'Here are your results for semester {}: {}'.format(session['semester'], results['marks'])})
            else:
                return jsonify({'response': 'No results found for {} in semester {}.'.format(session['email'], session['semester'])})
        except ValueError:
            return jsonify({'response': 'Please enter a valid number for the semester.'})

if __name__ == '__main__':
    app.run(debug=True)
