from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory data store
items = []

# Create
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data or 'price' not in data:
        abort(400, 'Name, description, and price are required')
    item = {
        'id': len(items) + 1,
        'name': data['name'],
        'description': data['description'],
        'price': data['price'],
        'created_at': datetime.now().isoformat()
    }
    items.append(item)
    return jsonify(item), 201

# Read all
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Read one
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        abort(404)
    return jsonify(item)

# Update
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        abort(404)
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data or 'price' not in data:
        abort(400, 'Name, description, and price are required')
    item['name'] = data['name']
    item['description'] = data['description']
    item['price'] = data['price']
    return jsonify(item)

# Delete
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        abort(404)
    items = [i for i in items if i['id'] != item_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5001)
