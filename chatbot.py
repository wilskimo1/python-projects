from flask import Blueprint, request, jsonify
import json

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api")  # Add URL prefix

# 🟢 Predefined chatbot responses
PREDEFINED_RESPONSES = {
    "hello": "Hi there! How can I help you today?",
    "how are you": "I'm doing great! How about you?",
    "what is your name": "I'm your friendly chatbot!",
    "bye": "Goodbye! Have a great day!",
    "help": "I'm here to assist you! Ask me anything.",
}

@chatbot_bp.route("/chatbot", methods=["POST"])  # Flask API Route
def chatbot():
    """Flask API that returns predefined chatbot responses."""
    try:
        body = request.json  # Get JSON payload from request
        user_message = body.get("message", "").strip().lower()

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Fetch response from predefined responses
        chatbot_reply = PREDEFINED_RESPONSES.get(user_message, "I'm not sure how to respond to that.")

        return jsonify({"response": chatbot_reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🟢 AWS Lambda Function (for API Gateway)
def lambda_handler(event, context):
    """AWS Lambda function that returns predefined chatbot responses."""
    try:
        # Parse request body
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "").strip().lower()

        if not user_message:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Message cannot be empty"})
            }

        # Fetch response from predefined responses
        chatbot_reply = PREDEFINED_RESPONSES.get(user_message, "I'm not sure how to respond to that.")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"response": chatbot_reply})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
