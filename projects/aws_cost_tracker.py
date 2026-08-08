from flask import Blueprint, render_template
import boto3
import datetime

aws_cost_tracker_bp = Blueprint("aws_cost_tracker", __name__)

# Use IAM role credentials from EC2 instance
ce_client = boto3.client("ce", region_name="us-east-1")


def get_aws_cost():
    """Retrieve AWS cost data from Cost Explorer."""
    try:
        today = datetime.date.today()
        start_date = today.replace(day=1)                    # First of current month
        end_date = today + datetime.timedelta(days=1)        # Tomorrow

        print(f"🔍 Requesting AWS cost from {start_date} to {end_date}")

        response = ce_client.get_cost_and_usage(
            TimePeriod={
                "Start": start_date.isoformat(),
                "End": end_date.isoformat()
            },
            Granularity="MONTHLY",
            Metrics=["BlendedCost"]
        )

        cost = response["ResultsByTime"][0]["Total"]["BlendedCost"]["Amount"]
        return float(cost)

    except Exception as e:
        import traceback
        print("❌ Exception occurred in get_aws_cost()")
        traceback.print_exc()
        return None


@aws_cost_tracker_bp.route("/")
def aws_cost_page():
    """Display AWS cost data in UI."""
    current_cost = get_aws_cost()

    if current_cost is None:
        alert_status = "⚠️ Unable to retrieve AWS cost data."
        css_class = "text-warning"
        cost_display = "N/A"
    elif current_cost > 100:
        alert_status = "🚨 ALERT: Budget Exceeded!"
        css_class = "text-danger"
        cost_display = f"{current_cost:.2f}"
    else:
        alert_status = "✅ OK - Currently within Budget"
        css_class = "text-success"
        cost_display = f"{current_cost:.2f}"

    return render_template(
        "aws_cost_tracker.html",
        cost_display=cost_display,
        alert_status=alert_status,
        css_class=css_class
    )
