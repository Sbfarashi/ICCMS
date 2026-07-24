from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from forms.update_complaint_form import UpdateComplaintForm

from services.staff_service import StaffService


staff = Blueprint(
    "staff",
    __name__
)


# ======================================================
# Staff Dashboard
# ======================================================

@staff.route("/staff/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") not in [
        "staff",
        "engineer",
        "technician",
        "support"
    ]:
        flash(
            "Access denied.",
            "danger"
        )
        return redirect(url_for("auth.login"))

    statistics = StaffService.get_dashboard_statistics(
        session["user_id"]
    )

    complaints = StaffService.get_assigned_complaints(
        session["user_id"]
    )

    return render_template(
        "staff/dashboard.html",
        statistics=statistics,
        complaints=complaints
    )


# ======================================================
# Complaint Details
# ======================================================

@staff.route("/staff/complaint/<int:complaint_id>")
def complaint_details(complaint_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    complaint = StaffService.get_complaint(
        complaint_id
    )

    if complaint is None:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for("staff.dashboard")
        )

    return render_template(
        "staff/complaint_details.html",
        complaint=complaint
    )


# ======================================================
# Update Complaint
# ======================================================

@staff.route(
    "/staff/update/<int:complaint_id>",
    methods=["GET", "POST"]
)
def update_complaint(complaint_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    complaint = StaffService.get_complaint(
        complaint_id
    )

    if complaint is None:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for("staff.dashboard")
        )

    form = UpdateComplaintForm()

    if form.validate_on_submit():

        success, message = StaffService.update_complaint(

            complaint_id=complaint.id,

            status=form.status.data,

            resolution=form.resolution.data,

            staff_id=session["user_id"]

        )

        flash(
            message,
            "success" if success else "danger"
        )

        if success:

            return redirect(
                url_for(
                    "staff.complaint_details",
                    complaint_id=complaint.id
                )
            )

    if not form.is_submitted():

        form.status.data = complaint.status
        form.resolution.data = complaint.resolution

    return render_template(
        "staff/update_complaint.html",
        form=form,
        complaint=complaint
    )