from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


# Create tables
with app.app_context():
    db.create_all()

# POST endpoint: Add user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({"error": "username and email are required"}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User with this email already exists"}), 400

    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully", "user": new_user.to_dict()}), 201


# GET endpoint: Fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


if __name__ == '__main__':
    app.run(debug=True)
