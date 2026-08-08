from flask import Blueprint, render_template, jsonify, current_app
import boto3
from flask_login import login_required, current_user

# ✅ Define the Blueprint
it_compliance_auditor_bp = Blueprint("it_compliance_auditor", __name__)

# ✅ Initialize AWS Security Hub client
securityhub = boto3.client("securityhub", region_name="us-east-1")

def get_compliance_findings():
    """Fetch compliance findings from AWS Security Hub."""
    try:
        response = securityhub.get_findings(
            Filters={"RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}]}
        )

        findings = []
        for item in response.get("Findings", []):
            findings.append({
                "title": item.get("Title", "No Title"),
                "severity": item.get("Severity", {}).get("Label", "Unknown"),
                "resource": item.get("Resources", [{}])[0].get("Id", "Unknown"),
                "description": item.get("Description", "No description available"),
                "recommendation": item.get("Remediation", {}).get("Recommendation", {}).get("Text", "No recommendation available")
            })

        return findings

    except Exception as e:
        current_app.logger.error(f"❌ Error fetching compliance findings: {str(e)}")
        return []  # ✅ Return empty list instead of an error JSON object

### 🔓 **Allow All Users to View the Page (No Login Required)**
@it_compliance_auditor_bp.route("/projects/it-compliance-auditor/page")
def compliance_page():
    """Render the IT Compliance Auditor page (Publicly Accessible)."""
    is_admin = current_user.is_authenticated  # ✅ Check if user is logged in
    current_app.logger.info(f"📄 Rendering IT Compliance Auditor page (is_admin={is_admin})")  # ✅ Use logging
    return render_template("it_compliance_auditor.html", is_admin=is_admin)

### 🔒 **Only Require Login for API Requests**
@it_compliance_auditor_bp.route("/api/compliance", methods=["GET"])
@login_required
def fetch_compliance_data():
    """API: Fetch compliance findings (Requires Login)."""
    findings = get_compliance_findings()
    return jsonify(findings)
