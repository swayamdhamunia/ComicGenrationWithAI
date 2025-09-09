from flask import Blueprint, request, jsonify


Loginapp = Blueprint('login', __name__)

# Mock user data (you can replace this with database validation)
users = {
    'swayam': '123',
    'user2': 'securepassword',
}

@Loginapp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Simple validation: check if username and password match
    if username in users and users[username] == password:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401


