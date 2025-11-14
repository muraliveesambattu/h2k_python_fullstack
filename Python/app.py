from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def to_dict(self, include_password=True):
        data = {
            "id": self.id,
            "username": self.username,
        }
        if include_password:
            data["password"] = self.password
        return data


# Create database tables
with app.app_context():
    db.create_all()


# POST endpoint to add user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Please provide username and password'}), 400

    # Check for duplicate username
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User added successfully",
        "user": new_user.to_dict()
    }), 201


# GET endpoint to fetch all users
@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict(include_password=False) for user in users]), 200


# DELETE endpoint to delete a user
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': f'User with id {id} does not exist'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User with id {id} deleted successfully'}), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
