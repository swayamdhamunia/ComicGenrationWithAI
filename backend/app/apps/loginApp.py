from flask import Blueprint, request, jsonify
import mysql.connector
import bcrypt
import jwt
import datetime

Loginapp = Blueprint('login', __name__)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shreem@2004',
    'database': 'comicgeneration'
}

# JWT secret key (this should be kept secret in a production environment)
SECRET_KEY = 'swayam_screte_key'

# Function to get the DB connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Function to generate JWT token
def generate_jwt_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)  # Token expiration in 15 minutes
    payload = {
        'username': username,
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # Encode the payload using the secret key
    return token


# Login route to handle user login
@Loginapp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Simple validation: check if username and password are provided
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    # Check if the user exists and if the password matches
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):  # Compare hashed passwords
                # Generate a JWT token upon successful login
                token = generate_jwt_token(username)

                # Return success response with the JWT token
                return jsonify({'status': 'success', 'message': 'Login successful', 'token': token}), 200  # Success response
            else:
                return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
        else:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': f"Database error: {err}"}), 500

    finally:
        cursor.close()
        connection.close()
