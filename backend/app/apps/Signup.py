from flask import Blueprint, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt

# Create the blueprint for signup
signup = Blueprint("signup", __name__)
CORS(signup)  # Allow cross-origin requests

# MySQL configuration (hardcoded for simplicity)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shreem@2004',
    'database': 'comicgeneration'
}

# Connect to MySQL database function
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Signup route to handle user registration
@signup.route('/signup', methods=['POST'])  # Use signup.route instead of app.route
def signup_user():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Print username and password for debugging (don't do this in production)
    print(f"Received username: {username}")
    print(f"Received password: {password}")

    # Basic validation
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    # Check if the user already exists in the database
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'status': 'error', 'message': 'Username already taken'}), 400

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # hashed_username = bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt())
        # Insert new user into the database with the hashed password
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()

        # Print success message
        print(f"User {username} created successfully.")
        
        return jsonify({'status': 'success', 'message': 'Account created successfully'}), 201
    except mysql.connector.Error as err:
        # In case of error, roll back the transaction and return an error
        connection.rollback()
        return jsonify({'status': 'error', 'message': f"Database error: {err}"}), 500
    finally:
        cursor.close()
        connection.close()
