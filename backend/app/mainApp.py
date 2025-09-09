from flask import Flask
from flask_cors import CORS
from apps.main import message_blueprint  # Import the blueprint
from apps.loginApp import Loginapp 
app = Flask(__name__)

# Enable CORS
CORS(app)

# Register the blueprint with the app
app.register_blueprint(message_blueprint)
app.register_blueprint(Loginapp)

if __name__ == "__main__":
    app.run(debug=True)
