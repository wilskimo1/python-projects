from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import boto3, logging

flask_resume_api_bp = Blueprint("flask_resume_api", __name__)
logging.basicConfig(level=logging.DEBUG)

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("resume_data")

### ✅ Public Resume Page
@flask_resume_api_bp.route("/")
def resume_page():
    from flask_login import current_user  # (optional, already imported above)

    # 🔍 Debug login state
    print(f"🧠 is_authenticated: {current_user.is_authenticated}")
    print(f"🆔 current_user.id: {current_user.get_id() if current_user.is_authenticated else 'Anonymous'}")

    return render_template("flask_resume_api.html", is_admin=current_user.is_authenticated)


### ✅ Fetch Resume (Public)
@flask_resume_api_bp.route("/api/resume", methods=["GET"])
def get_resume():
    try:
        response = table.get_item(Key={"user_id": "1"})
        logging.debug(f"🔍 DynamoDB Response: {response}")
        if "Item" in response:
            return jsonify(response["Item"]), 200, {'Cache-Control': 'no-store'}
        else:
            return jsonify({"error": "No resume found"}), 404
    except Exception as e:
        logging.error(f"❌ Error fetching resume: {e}")
        return jsonify({"error": str(e)}), 500

### ✅ Update Resume (Requires Login)
@flask_resume_api_bp.route("/api/resume", methods=["POST"])
@login_required
def update_resume():
    try:
        data = request.get_json()
        logging.debug(f"📤 Incoming resume update data: {data}")

        # Retrieve existing data
        response = table.get_item(Key={"user_id": "1"})
        existing_data = response.get("Item", {})
        if not existing_data:
            return jsonify({"error": "No existing resume data found"}), 404

        # ✅ Update relevant fields
        updated_resume = {
            "user_id": "1",
            "name": data.get("name", existing_data.get("name")),
            "email": data.get("email", existing_data.get("email")),
            "phone": data.get("phone", existing_data.get("phone")),
            "summary": data.get("summary", existing_data.get("summary")),
            "skills_col1_list": data.get("skills_col1_list", existing_data.get("skills_col1_list")),
            "skills_col2_list": data.get("skills_col2_list", existing_data.get("skills_col2_list")),
        }

        logging.debug(f"📝 Final resume payload to write: {updated_resume}")

        # ✅ Save to DynamoDB
        result = table.put_item(Item=updated_resume)
        logging.debug(f"✅ DynamoDB put_item response: {result}")

        return jsonify({
            "message": "✅ Resume updated successfully.",
            "updated_data": updated_resume
        }), 200

    except Exception as e:
        logging.error(f"❌ Error updating resume: {e}")
        return jsonify({"error": str(e)}), 500


