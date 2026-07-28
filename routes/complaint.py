from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from forms.complaint_form import ComplaintForm

from models.category import Category
from models.complaint import Complaint

from services.complaint_service import ComplaintService
from services.activity_log_service import ActivityLogService

complaint = Blueprint(
    "complaint",
    __name__
)


# ======================================================
# Submit Complaint
# ======================================================

@complaint.route(
    "/customer/submit-complaint",
    methods=["GET", "POST"]
)
def submit_complaint():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    form = ComplaintForm()

    # ==========================================
    # Load Categories
    # ==========================================

    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    form.category.choices = [

        (category.id, category.name)

        for category in categories

    ]

    if form.validate_on_submit():

        meter_number = request.form.get(
            "meter_number",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        success, message = ComplaintService.submit(

            customer_id=session["user_id"],

            form=form,

            meter_number=meter_number,

            location=location

        )

        if success:

            ActivityLogService.log(
                user_id=session["user_id"],
                activity="Submitted a new complaint",
                module="Complaint Management"
            )

        flash(

            message,

            "success" if success else "danger"

        )

        if success:

            return redirect(

                url_for("complaint.history")

            )

    return render_template(

        "customer/submit_complaint.html",

        form=form

    )


# ======================================================
# Complaint History
# ======================================================

@complaint.route("/customer/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    complaints = (

        Complaint.query

        .filter_by(

            customer_id=session["user_id"]

        )

        .order_by(

            Complaint.created_at.desc()

        )

        .all()

    )

    return render_template(

        "customer/history.html",

        complaints=complaints

    )