from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

DATA_FILE = 'users.json'

DEFAULT_USERS = [
    {"id": 1, "name": "Murali Veesambattu", "email": "murali@example.com"},
    {"id": 2, "name": "Rohit Sharma", "email": "rohit.sharma@example.com"},
    {"id": 3, "name": "Virat Kohli", "email": "virat.kohli@example.com"}
]
def load_users():
    save_users(DEFAULT_USERS)
    with open(DATA_FILE, 'r') as f:
        users = json.load(f)
    return users

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def index():
    users = load_users()
    return render_template('index.html',users=users)

if __name__=='__main__':
    app.run(debug=True)