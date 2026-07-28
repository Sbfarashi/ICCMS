from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from decorators.auth import (
    login_required,
    staff_required
)

from forms.staff_forms import (
    AssignEngineerForm,
    UpdateStatusForm,
    StaffProfileForm
)

from services.staff_service import StaffService


staff = Blueprint(
    "staff",
    __name__,
    url_prefix="/staff"
)


# ==========================================================
# STAFF DASHBOARD
# ==========================================================

@staff.route("/dashboard")
@login_required
@staff_required
def dashboard():

    user_id = session["user_id"]

    statistics = StaffService.my_dashboard_statistics(
        user_id
    )

    complaints = StaffService.my_assigned_complaints(
        user_id
    )

    return render_template(
        "staff/dashboard.html",
        statistics=statistics,
        complaints=complaints
    )


# ==========================================================
# MY ASSIGNED COMPLAINTS
# ==========================================================

@staff.route("/my-complaints")
@login_required
@staff_required
def my_complaints():

    user_id = session["user_id"]

    search = request.args.get(
        "search",
        ""
    ).strip()

    status = request.args.get(
        "status",
        ""
    ).strip()

    priority = request.args.get(
        "priority",
        ""
    ).strip()

    sort = request.args.get(
        "sort",
        "newest"
    )

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    complaints = StaffService.search_my_complaints(
        user_id=user_id,
        search=search,
        status=status,
        priority=priority,
        sort=sort,
        page=page
    )

    return render_template(
        "staff/my_complaints.html",
        complaints=complaints,
        search=search,
        status=status,
        priority=priority,
        sort=sort
    )


# ==========================================================
# COMPLAINT DETAILS
# ==========================================================

@staff.route("/complaint/<int:complaint_id>")
@login_required
@staff_required
def complaint_details(complaint_id):

    complaint = StaffService.get_complaint(
        complaint_id
    )

    if complaint is None:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for("staff.my_complaints")
        )

    history = StaffService.complaint_history(
        complaint_id
    )

    return render_template(
        "staff/complaint_details.html",
        complaint=complaint,
        history=history
    )


# ==========================================================
# ASSIGN ENGINEER
# ==========================================================

@staff.route(
    "/assign-engineer/<int:complaint_id>",
    methods=["GET", "POST"]
)
@login_required
@staff_required
def assign_engineer(complaint_id):

    complaint = StaffService.get_complaint(
        complaint_id
    )

    if complaint is None:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for("staff.my_complaints")
        )

    form = AssignEngineerForm()

    engineers = StaffService.get_staff_users()

    form.engineer_id.choices = [

        (
            engineer.id,
            engineer.full_name
        )

        for engineer in engineers

    ]

    if form.validate_on_submit():

        StaffService.assign_complaint(

            complaint_id=complaint.id,

            staff_id=form.engineer_id.data,

            performed_by=session["user_id"]

        )

        flash(
            "Engineer assigned successfully.",
            "success"
        )

        return redirect(

            url_for(

                "staff.complaint_details",

                complaint_id=complaint.id

            )

        )

    history = StaffService.complaint_history(
        complaint.id
    )

    return render_template(
        "staff/assign_engineer.html",
        complaint=complaint,
        form=form,
        history=history
    )


# ==========================================================
# UPDATE COMPLAINT STATUS
# ==========================================================

@staff.route(
    "/update-status/<int:complaint_id>",
    methods=["GET", "POST"]
)
@login_required
@staff_required
def update_status(complaint_id):

    complaint = StaffService.get_complaint(
        complaint_id
    )

    if complaint is None:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for("staff.my_complaints")
        )

    form = UpdateStatusForm()

    if form.validate_on_submit():

        StaffService.update_status(

            complaint_id=complaint.id,

            status=form.status.data,

            performed_by=session["user_id"],

            remarks=form.remarks.data

        )

        flash(
            "Complaint status updated successfully.",
            "success"
        )

        return redirect(

            url_for(

                "staff.complaint_details",

                complaint_id=complaint.id

            )

        )

    if request.method == "GET":

        form.status.data = complaint.status

    history = StaffService.complaint_history(
        complaint.id
    )

    return render_template(
        "staff/update_status.html",
        complaint=complaint,
        form=form,
        history=history
    )


# ==========================================================
# RESOLVE COMPLAINT
# ==========================================================

@staff.route(
    "/resolve/<int:complaint_id>",
    methods=["GET", "POST"]
)
@login_required
@staff_required
def resolve_complaint(complaint_id):

    complaint = StaffService.get_complaint(
        complaint_id
    )

    if complaint is None:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for("staff.my_complaints")
        )

    if request.method == "POST":

        resolution = request.form.get(
            "resolution",
            ""
        ).strip()

        if not resolution:

            flash(
                "Resolution cannot be empty.",
                "warning"
            )

            return redirect(

                url_for(

                    "staff.resolve_complaint",

                    complaint_id=complaint.id

                )

            )

        StaffService.add_resolution(

            complaint.id,

            resolution,

            session["user_id"]

        )

        flash(
            "Complaint resolved successfully.",
            "success"
        )

        return redirect(

            url_for(

                "staff.complaint_details",

                complaint_id=complaint.id

            )

        )

    history = StaffService.complaint_history(
        complaint.id
    )

    return render_template(
        "staff/resolve_complaint.html",
        complaint=complaint,
        history=history
    )


# ==========================================================
# STAFF WORKLOAD
# ==========================================================

@staff.route("/workload")
@login_required
@staff_required
def workload():

    workload = StaffService.staff_workload()

    return render_template(
        "staff/workload.html",
        workload=workload
    )


# ==========================================================
# REPORTS
# ==========================================================

@staff.route("/reports")
@login_required
@staff_required
def reports():

    statistics = StaffService.dashboard_statistics()

    complaints = StaffService.search_complaints()

    return render_template(
        "staff/reports.html",
        statistics=statistics,
        complaints=complaints
    )