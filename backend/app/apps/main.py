from flask import Blueprint, request, jsonify
import time

# Define the Blueprint
message_blueprint = Blueprint('messages', __name__)

class Message:
    def __init__(self, text, sender):
        self.text = text
        self.sender = sender

    def to_dict(self):
        return {
            "text": self.text,
            "sender": self.sender
        }

@message_blueprint.route("/send-message/", methods=["POST"])
def send_message():
    try:
        # Extract message data from the request
        data = request.get_json()

        if "text" not in data or "sender" not in data:
            return jsonify({"detail": "Missing 'text' or 'sender'"}), 400

        message = Message(text=data["text"], sender=data["sender"])

        # Simulate processing time
        if message.sender == "user":
            time.sleep(1)  # simulate processing delay
            return jsonify({
                "text": "Generating pdf of comic.",
                "sender": "bot"
            })
        else:
            return jsonify({"detail": "Invalid message sender"}), 400

    except Exception as e:
        return jsonify({"detail": str(e)}), 500
