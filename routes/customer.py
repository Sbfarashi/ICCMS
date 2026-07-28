from flask import Blueprint, render_template, session
from models.complaint import Complaint

customer = Blueprint("customer", __name__)


@customer.route("/dashboard")
def dashboard():
    user_id = session["user_id"]

    # Base query
    base_query = Complaint.query.filter_by(customer_id=user_id)

    # Recent complaints
    complaints = (
        base_query
        .order_by(Complaint.created_at.desc())
        .limit(5)
        .all()
    )

    # Dashboard statistics
    total = base_query.count()

    pending = base_query.filter_by(
        status="Pending"
    ).count()

    resolved = base_query.filter_by(
        status="Resolved"
    ).count()

    escalated = base_query.filter_by(
        status="Escalated"
    ).count()

    return render_template(
        "customer/dashboard.html",
        complaints=complaints,
        total_complaints=total,
        pending=pending,
        resolved=resolved,
        escalated=escalated
    )