from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from utils.aws_helpers import upload_file_to_s3, list_files_in_s3, delete_file_from_s3

# S3 Bucket Name (Fix the incorrect reference)
S3_BUCKET_NAME = "skimos-flask-app"

# Create Blueprint
s3_file_manager_bp = Blueprint("s3_file_manager", __name__, template_folder="templates")

# ✅ Route: S3 File Manager Dashboard (Requires Login)
@s3_file_manager_bp.route("/s3-file-manager")
@login_required
def s3_dashboard():
    """Render S3 File Manager Page."""
    return render_template("s3_file_manager.html", is_admin=current_user.is_authenticated)

# ✅ Route: List Files in S3 (Requires Login)
@s3_file_manager_bp.route("/api/s3/list", methods=["GET"])
@login_required
def list_files():
    """List files in the S3 bucket."""
    print(f"🔍 Debugging Current User: {current_user}")
    print(f"🔍 Is Authenticated: {current_user.is_authenticated}")

    if not current_user.is_authenticated:
        return jsonify({"error": "User is not authenticated"}), 403

    try:
        files = list_files_in_s3(S3_BUCKET_NAME)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Route: Upload File to S3 (Requires Login)
@s3_file_manager_bp.route("/api/s3/upload", methods=["POST"])
@login_required
def upload_file():
    """Upload a file to S3."""
    if "file" not in request.files:
        print("❌ No file part in request!")
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    file_name = file.filename

    if file_name == "":
        print("❌ No file selected!")
        return jsonify({"error": "No selected file"}), 400

    print(f"📤 Uploading {file_name} to S3...")

    try:
        result = upload_file_to_s3(file, file_name)
        print("✅ Upload Successful:", result)
        return jsonify(result), 201 if "file_url" in result else 500
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        return jsonify({"error": str(e)}), 500


# ✅ Route: Delete File from S3 (Requires Login)
@s3_file_manager_bp.route("/api/s3/delete", methods=["POST"])
@login_required
def delete_file():
    """Delete a file from S3."""
    data = request.get_json()
    file_name = data.get("file_name")

    if not file_name:
        return jsonify({"error": "Missing file name"}), 400

    try:
        result = delete_file_from_s3(file_name, S3_BUCKET_NAME)
        return jsonify(result), 200 if "message" in result else 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
