from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB Connection
client = MongoClient("mongodb+srv://Kishan:luka2000@cluster0.2g59arm.mongodb.net/")
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
        return jsonify({'response': f'Hi, {session["name"]}! Please provide your email.'})

    # Step 2: Ask for Email
    elif session['step'] == 2:
        session['email'] = message
        session['step'] = 3
        return jsonify({'response': f'Thanks, {session["name"]}! Now please select your semester from 1-8.', 'options': list(range(1, 9))})

    # Step 3: Get Semester
    elif session['step'] == 3:
        try:
            semester = int(message)
            if semester not in range(1, 9):
                # Invalid semester, reset and start from the beginning
                session['step'] = 1
                session['name'] = None
                session['email'] = None
                session['semester'] = None
                return jsonify({'response': 'Invalid semester. Let\'s start again. What is your name?'})

            session['semester'] = semester

            # Fetch the result from MongoDB
            results = marks_collection.find_one({'email': session['email'], 'semester': session['semester']})

            if results:
                marks = results['marks']
                formatted_marks = [f"{subject}: {marks[subject]}" for subject in marks]
                # Return the results and then reset the session to start from the beginning
                session['step'] = 1
                session['name'] = None
                session['email'] = None
                session['semester'] = None
                return jsonify({'response': f'Here are your results for semester {session["semester"]}:', 'marks': formatted_marks})
            else:
                # No results found, reset and start from the beginning
                session['step'] = 1
                session['name'] = None
                session['email'] = None
                session['semester'] = None
                return jsonify({'response': f'No results found for {session["email"]} in semester {session["semester"]}. Let\'s start again. What is your name?'})
        except ValueError:
            # Invalid input, reset and start from the beginning
            session['step'] = 1
            session['name'] = None
            session['email'] = None
            session['semester'] = None
            return jsonify({'response': 'Invalid input. Let\'s start again. What is your name?'})

    # Default response if none of the conditions match
    session['step'] = 1
    session['name'] = None
    session['email'] = None
    session['semester'] = None
    return jsonify({'response': 'An error occurred. Let\'s start again. What is your name?'})

if __name__ == '__main__':
    app.run(debug=True)
