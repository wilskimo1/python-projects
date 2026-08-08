from flask import Blueprint, render_template, jsonify
import boto3
from datetime import datetime, timedelta, timezone  # ✅ Import timezone
from flask_login import login_required, current_user
from utils.aws_helpers import cloudwatch  # ✅ Import shared AWS resources

# Create Blueprint
infra_monitoring_bp = Blueprint("infra_monitoring", __name__)

# Initialize AWS CloudWatch Client
cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

def get_ec2_cpu_utilization():
    """Fetch CPU utilization metrics for EC2 instances from AWS CloudWatch."""
    try:
        response = cloudwatch.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": "cpuUtilization",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": "AWS/EC2",
                            "MetricName": "CPUUtilization",
                            "Dimensions": [{"Name": "InstanceId", "Value": "i-0db2e74160c4273e5"}]
                        },
                        "Period": 300,  # 5-minute intervals
                        "Stat": "Average"
                    },
                    "ReturnData": True
                }
            ],
            # ✅ Fixed Syntax: Added missing comma
            StartTime=(datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            EndTime=datetime.now(timezone.utc).isoformat()
        )

        if "MetricDataResults" in response and response["MetricDataResults"]:
            cpu_data = response["MetricDataResults"][0]["Values"]
            return {"cpu_utilization": round(cpu_data[-1], 2) if cpu_data else "No Data"}
        
        return {"error": "No CPU Utilization data found"}

    except Exception as e:
        return {"error": str(e)}

@infra_monitoring_bp.route("/")
def monitoring_dashboard():
    """Render Infrastructure Monitoring Dashboard page (No login required)."""
    is_logged_in = current_user.is_authenticated  # ✅ Check login state
    return render_template("infra_monitoring_dashboard.html", is_admin=is_logged_in)


@infra_monitoring_bp.route("/api/monitoring", methods=["GET"])
@login_required
def fetch_monitoring_data():
    """API: Fetch AWS Infrastructure Monitoring Data."""
    monitoring_data = get_ec2_cpu_utilization()
    return jsonify(monitoring_data)
