from flask import Blueprint, request, jsonify
import time
import os
from werkzeug.utils import secure_filename

# Create Blueprint
message_blueprint = Blueprint('messages', __name__)

# Uploads folder (ensure this exists or is created)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

        # Simulate processing time
        time.sleep(1)

        # Return bot response
        return jsonify({
            "text": "Generating PDF of comic." if image else "Processing your message.",
            "sender": "bot"
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500
