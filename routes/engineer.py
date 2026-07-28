from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    flash,

    session

)

from decorators.auth import login_required
from decorators.roles import engineer_required

from services.engineer_service import EngineerService
from forms.edit_profile_form import EditProfileForm
from forms.profile_picture_form import ProfilePictureForm
engineer_bp = Blueprint(

    "engineer",

    __name__,

    url_prefix="/engineer"

)


# ==========================================================
# ENGINEER DASHBOARD
# ==========================================================

@engineer_bp.route("/dashboard")
@login_required
@engineer_required
def dashboard():

    user_id = session["user_id"]

    statistics = EngineerService.dashboard_statistics(
        user_id
    )

    performance = EngineerService.performance(
        user_id
    )

    recent_jobs = EngineerService.recent_jobs(
        user_id
    )

    recent_visits = EngineerService.recent_field_visits(
        user_id
    )

    return render_template(

        "engineer/dashboard.html",

        statistics=statistics,

        performance=performance,

        recent_jobs=recent_jobs,

        recent_visits=recent_visits

    )


# ==========================================================
# MY JOBS
# ==========================================================

@engineer_bp.route("/jobs")
@login_required
@engineer_required
def my_jobs():

    page = request.args.get(

        "page",

        1,

        type=int

    )

    search = request.args.get(

        "search",

        ""

    )

    status = request.args.get(

        "status",

        ""

    )

    priority = request.args.get(

        "priority",

        ""

    )

    sort = request.args.get(

        "sort",

        "newest"

    )

    jobs = EngineerService.search_jobs(

        user_id=session["user_id"],

        search=search,

        status=status,

        priority=priority,

        sort=sort,

        page=page

    )

    return render_template(

        "engineer/my_jobs.html",

        jobs=jobs,

        search=search,

        status=status,

        priority=priority,

        sort=sort

    )


# ==========================================================
# JOB DETAILS
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>")
@login_required
@engineer_required
def complaint_details(complaint_id):

    complaint = EngineerService.get_job(
        complaint_id
    )

    history = EngineerService.complaint_history(
        complaint_id
    )

    visits = EngineerService.field_visits(
        complaint_id
    )

    return render_template(

        "engineer/complaint_details.html",

        complaint=complaint,

        history=history,

        visits=visits

    )
# ==========================================================
# START WORK
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/start", methods=["POST"])
@login_required
@engineer_required
def start_work(complaint_id):

    EngineerService.start_work(

        complaint_id,

        session["user_id"]

    )

    flash(

        "Work started successfully.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )


# ==========================================================
# ARRIVED AT SITE
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/arrive", methods=["POST"])
@login_required
@engineer_required
def arrive_site(complaint_id):

    EngineerService.arrived_at_site(

        complaint_id,

        session["user_id"]

    )

    flash(

        "Arrival recorded successfully.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )


# ==========================================================
# INSPECTION STARTED
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/inspection", methods=["POST"])
@login_required
@engineer_required
def inspection_started(complaint_id):

    EngineerService.inspection_started(

        complaint_id,

        session["user_id"]

    )

    flash(

        "Inspection started.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )


# ==========================================================
# METER TESTED
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/meter-test", methods=["POST"])
@login_required
@engineer_required
def meter_tested(complaint_id):

    remarks = request.form.get(

        "remarks",

        "Meter tested successfully."

    )

    EngineerService.meter_tested(

        complaint_id,

        session["user_id"],

        remarks

    )

    flash(

        "Meter test recorded.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )


# ==========================================================
# WIRING CHECK
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/wiring", methods=["POST"])
@login_required
@engineer_required
def wiring_checked(complaint_id):

    remarks = request.form.get(

        "remarks",

        "Customer wiring inspected."

    )

    EngineerService.wiring_checked(

        complaint_id,

        session["user_id"],

        remarks

    )

    flash(

        "Wiring inspection recorded.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )


# ==========================================================
# UPDATE STATUS
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/status", methods=["POST"])
@login_required
@engineer_required
def update_status(complaint_id):

    status = request.form.get(

        "status"

    )

    remarks = request.form.get(

        "remarks",

        ""

    )

    EngineerService.update_status(

        complaint_id,

        status,

        session["user_id"],

        remarks

    )

    flash(

        "Complaint status updated successfully.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )
# ==========================================================
# RECORD FIELD VISIT
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/field-visit", methods=["GET", "POST"])
@login_required
@engineer_required
def field_visit(complaint_id):

    complaint = EngineerService.get_job(
        complaint_id
    )

    if request.method == "POST":

        EngineerService.create_field_visit(

            complaint_id=complaint_id,

            engineer_id=session["user_id"],

            visit_date=request.form.get("visit_date"),

            arrival_time=request.form.get("arrival_time"),

            departure_time=request.form.get("departure_time"),

            observations=request.form.get("observations"),

            root_cause=request.form.get("root_cause"),

            work_done=request.form.get("work_done"),

            materials_used=request.form.get("materials_used"),

            meter_replaced=True if request.form.get("meter_replaced") else False,

            old_meter_number=request.form.get("old_meter_number"),

            new_meter_number=request.form.get("new_meter_number"),

            recommendation=request.form.get("recommendation")

        )

        flash(

            "Field visit recorded successfully.",

            "success"

        )

        return redirect(

            url_for(

                "engineer.complaint_details",

                complaint_id=complaint_id

            )

        )

    return render_template(

        "engineer/field_visit.html",

        complaint=complaint

    )


# ==========================================================
# EDIT FIELD VISIT
# ==========================================================

@engineer_bp.route("/field-visit/<int:visit_id>/edit", methods=["GET", "POST"])
@login_required
@engineer_required
def edit_field_visit(visit_id):

    visit = EngineerService.get_field_visit(
        visit_id
    )

    if request.method == "POST":

        EngineerService.update_field_visit(

            visit_id=visit.id,

            visit_date=request.form.get("visit_date"),

            arrival_time=request.form.get("arrival_time"),

            departure_time=request.form.get("departure_time"),

            observations=request.form.get("observations"),

            root_cause=request.form.get("root_cause"),

            work_done=request.form.get("work_done"),

            materials_used=request.form.get("materials_used"),

            recommendation=request.form.get("recommendation"),

            meter_replaced=True if request.form.get("meter_replaced") else False,

            old_meter_number=request.form.get("old_meter_number"),

            new_meter_number=request.form.get("new_meter_number")

        )

        flash(

            "Field visit updated successfully.",

            "success"

        )

        return redirect(

            url_for(

                "engineer.complaint_details",

                complaint_id=visit.complaint_id

            )

        )

    return render_template(

        "engineer/edit_field_visit.html",

        visit=visit

    )


# ==========================================================
# DELETE FIELD VISIT
# ==========================================================

@engineer_bp.route("/field-visit/<int:visit_id>/delete", methods=["POST"])
@login_required
@engineer_required
def delete_field_visit(visit_id):

    visit = EngineerService.get_field_visit(
        visit_id
    )

    complaint_id = visit.complaint_id

    EngineerService.delete_field_visit(
        visit_id
    )

    flash(

        "Field visit deleted successfully.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )


# ==========================================================
# REPLACE METER
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/replace-meter", methods=["POST"])
@login_required
@engineer_required
def replace_meter(complaint_id):

    EngineerService.replace_meter(

        complaint_id,

        session["user_id"],

        request.form.get("old_meter"),

        request.form.get("new_meter")

    )

    flash(

        "Meter replacement recorded successfully.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )


# ==========================================================
# SUBMIT RESOLUTION
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/resolution", methods=["GET", "POST"])
@login_required
@engineer_required
def resolution_report(complaint_id):

    complaint = EngineerService.get_job(
        complaint_id
    )

    if request.method == "POST":

        EngineerService.submit_resolution(

            complaint_id,

            request.form.get("resolution"),

            session["user_id"]

        )

        flash(

            "Resolution submitted successfully.",

            "success"

        )

        return redirect(

            url_for(

                "engineer.complaint_details",

                complaint_id=complaint_id

            )

        )

    return render_template(

        "engineer/resolution_report.html",

        complaint=complaint

    )
# ==========================================================
# CLOSE JOB
# ==========================================================

@engineer_bp.route("/job/<int:complaint_id>/close", methods=["POST"])
@login_required
@engineer_required
def close_job(complaint_id):

    EngineerService.close_job(

        complaint_id,

        session["user_id"]

    )

    flash(

        "Complaint closed successfully.",

        "success"

    )

    return redirect(

        url_for(

            "engineer.complaint_details",

            complaint_id=complaint_id

        )

    )


# ==========================================================
# MY FIELD VISITS
# ==========================================================

@engineer_bp.route("/field-visits")
@login_required
@engineer_required
def my_field_visits():

    visits = EngineerService.my_field_visits(

        session["user_id"]

    )

    return render_template(

        "engineer/my_field_visits.html",

        visits=visits

    )


# ==========================================================
# ENGINEER PERFORMANCE
# ==========================================================

@engineer_bp.route("/performance")
@login_required
@engineer_required
def performance():

    performance = EngineerService.performance(

        session["user_id"]

    )

    monthly_statistics = EngineerService.monthly_statistics(

        session["user_id"]

    )

    average_resolution_time = EngineerService.average_resolution_time(

        session["user_id"]

    )

    return render_template(

        "engineer/performance.html",

        performance=performance,

        monthly_statistics=monthly_statistics,

        average_resolution_time=average_resolution_time

    )


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

@engineer_bp.route("/summary")
@login_required
@engineer_required
def summary():

    summary = EngineerService.dashboard_summary(

        session["user_id"]

    )

    return render_template(

        "engineer/summary.html",

        summary=summary

    )


# ==========================================================
# WORKLOAD
# ==========================================================

@engineer_bp.route("/workload")
@login_required
@engineer_required
def workload():

    workload = EngineerService.workload(

        session["user_id"]

    )

    return render_template(

        "engineer/workload.html",

        workload=workload

    )


# ==========================================================
# ACTIVITY HISTORY
# ==========================================================

@engineer_bp.route("/activities")
@login_required
@engineer_required
def activities():

    activities = EngineerService.activity_summary(

        session["user_id"]

    )

    return render_template(

        "engineer/activities.html",

        activities=activities

    )


# ==========================================================
# OPEN JOBS
# ==========================================================

@engineer_bp.route("/open-jobs")
@login_required
@engineer_required
def open_jobs():

    jobs = EngineerService.open_jobs(

        session["user_id"]

    )

    return render_template(

        "engineer/open_jobs.html",

        jobs=jobs

    )


# ==========================================================
# COMPLETED JOBS
# ==========================================================

@engineer_bp.route("/completed-jobs")
@login_required
@engineer_required
def completed_jobs():

    jobs = EngineerService.completed_jobs(

        session["user_id"]

    )

    return render_template(

        "engineer/completed_jobs.html",

        jobs=jobs

    )
# ==========================================================
# ENGINEER PROFILE
# ==========================================================

@engineer_bp.route("/profile")
@login_required
@engineer_required
def profile():

    user_id = session["user_id"]

    engineer = EngineerService.engineer_profile(user_id)

    stats = {
        "total_jobs": EngineerService.performance(user_id)["total"],
        "open_jobs": EngineerService.count_open_jobs(user_id),
        "completed_jobs": EngineerService.count_completed_jobs(user_id),
        "field_visits": EngineerService.total_field_visits(user_id)
    }

    picture_form = ProfilePictureForm()

    return render_template(
        "engineer/profile.html",
        engineer=engineer,
        stats=stats,
        picture_form=picture_form
    )
# ==========================================================
# EDIT ENGINEER PROFILE
# ==========================================================

@engineer_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
@engineer_required
def edit_profile():

    user_id = session["user_id"]

    engineer = EngineerService.engineer_profile(user_id)

    form = EditProfileForm(obj=engineer)

    if form.validate_on_submit():

        success, message = EngineerService.update_profile(
            user_id,
            form
        )

        if success:

            flash(message, "success")

            return redirect(
                url_for("engineer.profile")
            )

        flash(message, "danger")

    return render_template(
        "engineer/edit_profile.html",
        form=form,
        engineer=engineer
    )
# ==========================================================
# UPLOAD PROFILE PICTURE
# ==========================================================

@engineer_bp.route(
    "/upload-profile-picture",
    methods=["POST"]
)
@login_required
@engineer_required
def upload_profile_picture():

    form = ProfilePictureForm()

    if form.validate_on_submit():

        success, message = EngineerService.upload_profile_picture(
            session["user_id"],
            form.profile_picture.data
        )

        if success:
            flash(message, "success")
        else:
            flash(message, "danger")

    else:

        for errors in form.errors.values():
            for error in errors:
                flash(error, "danger")

    return redirect(
        url_for("engineer.profile")
    )
# ==========================================================
# VIEW FIELD VISIT DETAILS
# ==========================================================

@engineer_bp.route("/field-visit/<int:visit_id>")
@login_required
@engineer_required
def view_field_visit(visit_id):

    visit = EngineerService.get_field_visit(
        visit_id
    )

    return render_template(
        "engineer/view_field_visit.html",
        visit=visit
    )


# ==========================================================
# TODAY'S SUMMARY
# ==========================================================

@engineer_bp.route("/today")
@login_required
@engineer_required
def today_summary():

    return render_template(

        "engineer/today_summary.html",

        resolved_today=EngineerService.resolved_today(
            session["user_id"]
        ),

        closed_today=EngineerService.closed_today(
            session["user_id"]
        ),

        open_jobs=EngineerService.count_open_jobs(
            session["user_id"]
        ),

        completed_jobs=EngineerService.count_completed_jobs(
            session["user_id"]
        )

    )


# ==========================================================
# MONTHLY REPORT
# ==========================================================

@engineer_bp.route("/monthly-report")
@login_required
@engineer_required
def monthly_report():

    report = EngineerService.monthly_statistics(
        session["user_id"]
    )

    return render_template(
        "engineer/monthly_report.html",
        report=report
    )


# ==========================================================
# JSON DASHBOARD API
# ==========================================================

@engineer_bp.route("/api/dashboard")
@login_required
@engineer_required
def dashboard_api():

    return EngineerService.dashboard_summary(
        session["user_id"]
    )


# ==========================================================
# JSON PERFORMANCE API
# ==========================================================

@engineer_bp.route("/api/performance")
@login_required
@engineer_required
def performance_api():

    return EngineerService.performance(
        session["user_id"]
    )


# ==========================================================
# END OF ENGINEER ROUTES
# ==========================================================