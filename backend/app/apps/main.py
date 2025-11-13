from flask import Blueprint, request, jsonify
import time
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from . import pip_init
# Create Blueprint
message_blueprint = Blueprint('messages', __name__)

# Uploads folder (ensure this exists or is created)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Folder to save user text messages
TEXT_SAVE_FOLDER = 'user_texts'
os.makedirs(TEXT_SAVE_FOLDER, exist_ok=True)

@message_blueprint.route("/send-message/", methods=["POST"])
def send_message():
    try:
        # Get form data
        text = request.form.get("text")
        sender = request.form.get("sender")
        image = request.files.get("image")

        # Validation
        if not sender:
            return jsonify({"detail": "Missing 'sender'"}), 400

        if sender != "user":
            return jsonify({"detail": "Invalid sender"}), 400

        # If image is sent
        if image:
            filename = secure_filename(image.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)
            print(f"Image received and saved: {filename}")

        # If text is sent
        if text:
            print(f"Text received: {text}")

            # Save the text to a .txt file with a timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"user_message_{timestamp}.txt"
            filepath = os.path.join(TEXT_SAVE_FOLDER, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"User text saved: {filepath}")
            pip_init.hello_from_init()
            time.sleep(1)
            return jsonify({
                "text": "Generating your comic",
                "head": "Good things take time",
                "sender": "bot"
            })

        # Default response if only image or nothing sent
        time.sleep(1)
        return jsonify({
            "text": "Generating PDF of comic.",
            "sender": "bot"
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500
