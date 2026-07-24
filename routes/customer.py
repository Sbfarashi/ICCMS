from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from models.complaint import Complaint

customer = Blueprint(
    "customer",
    __name__
)


@customer.route("/dashboard")
def dashboard():
    """
    Customer Dashboard
    """

    # ======================================================
    # Check Login
    # ======================================================
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session.get("user_id")

    # ======================================================
    # Complaint Statistics
    # ======================================================
    total = Complaint.query.filter_by(
        customer_id=user_id
    ).count()

    pending = Complaint.query.filter_by(
        customer_id=user_id,
        status="Pending"
    ).count()

    resolved = Complaint.query.filter_by(
        customer_id=user_id,
        status="Resolved"
    ).count()

    escalated = Complaint.query.filter_by(
        customer_id=user_id,
        status="Escalated"
    ).count()

    # ======================================================
    # Recent Complaints
    # ======================================================
    complaints = (
        Complaint.query
        .filter_by(customer_id=user_id)
        .order_by(Complaint.created_at.desc())
        .limit(10)
        .all()
    )

    # ======================================================
    # Render Dashboard
    # ======================================================
    return render_template(
        "customer/dashboard.html",
        user_name=session.get("user_name", "Customer"),
        full_name=session.get("full_name", "Customer"),
        total_complaints=total,
        pending_complaints=pending,
        resolved_complaints=resolved,
        escalated_complaints=escalated,
        complaints=complaints
    )