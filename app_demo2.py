from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'users.json'

# Create JSON file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    # Read existing data safely
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []  # start with empty list if file is empty or invalid

    # Append new record
    data.append({'username': username, 'password': password})

    # Save back to file
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({'message': 'User saved successfully!', 'data': data})

if __name__ == '__main__':
    app.run(debug=True)
