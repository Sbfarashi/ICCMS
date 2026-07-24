from decorators.auth import admin_required
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from models.category import Category
from models.complaint import Complaint

from forms.assign_complaint_form import AssignComplaintForm
from forms.search_form import SearchForm
from forms.update_complaint_form import UpdateComplaintForm

from services.admin_service import AdminService
from services.admin_update_service import AdminUpdateService
from services.assignment_service import AssignmentService
from services.search_service import SearchService
from services.escalation_service import EscalationService
from services.performance_service import PerformanceService


admin = Blueprint(
    "admin",
    __name__
)


# ==========================================================
# DASHBOARD
# ==========================================================

@admin.route("/admin/dashboard")
@admin_required
def dashboard():

    # -----------------------------------------
    # Run Automatic Escalation
    # -----------------------------------------

    EscalationService.run()

    dashboard = AdminService.dashboard()

    return render_template(

        "admin/dashboard.html",

        dashboard=dashboard,

        priority=AdminService.complaints_by_priority(),

        status=AdminService.complaints_by_status()

    )


# ==========================================================
# COMPLAINT MANAGEMENT
# ==========================================================

@admin.route("/admin/complaints")
@admin_required
def complaints():

    EscalationService.run()

    form = SearchForm(request.args)

    # -------------------------------------
    # Load categories dynamically
    # -------------------------------------

    form.category.choices = [

        ("", "All Categories")

    ] + [

        (category.name, category.name)

        for category in

        Category.query.order_by(
            Category.name
        ).all()

    ]

    # -------------------------------------
    # Current page
    # -------------------------------------

    page = request.args.get(
        "page",
        1,
        type=int
    )

    # -------------------------------------
    # Search filters
    # -------------------------------------

    filters = {

        "complaint_number":
            request.args.get(
                "complaint_number",
                ""
            ),

        "customer":
            request.args.get(
                "customer",
                ""
            ),

        "meter_number":
            request.args.get(
                "meter_number",
                ""
            ),

        "status":
            request.args.get(
                "status",
                ""
            ),

        "priority":
            request.args.get(
                "priority",
                ""
            ),

        "category":
            request.args.get(
                "category",
                ""
            ),

        "date_from":
            request.args.get(
                "date_from",
                ""
            ),

        "date_to":
            request.args.get(
                "date_to",
                ""
            )

    }

    complaints = (

        SearchService.search(filters)

        .paginate(

            page=page,

            per_page=10,

            error_out=False

        )

    )

    return render_template(

        "admin/complaints.html",

        form=form,

        complaints=complaints,

        filters=filters

    )
    
    # ==========================================================
# COMPLAINT DETAILS
# ==========================================================

@admin.route("/admin/complaint/<int:complaint_id>")
@admin_required
def complaint_details(complaint_id):

    complaint = Complaint.query.get_or_404(
        complaint_id
    )

    return render_template(

        "admin/complaint_details.html",

        complaint=complaint

    )


# ==========================================================
# ASSIGN COMPLAINT
# ==========================================================

@admin.route(
    "/admin/assign/<int:complaint_id>",
    methods=["GET", "POST"]
)
@admin_required
def assign_complaint(complaint_id):

    complaint = Complaint.query.get_or_404(
        complaint_id
    )

    form = AssignComplaintForm()

    staff = AssignmentService.get_staff()

    form.staff.choices = [

        (user.id, user.full_name)

        for user in staff

    ]

    if form.validate_on_submit():

        success, message = AssignmentService.assign_complaint(

            complaint_id=complaint.id,

            staff_id=form.staff.data,

            admin_id=session["user_id"]

        )

        flash(

            message,

            "success" if success else "danger"

        )

        if success:

            return redirect(

                url_for(

                    "admin.complaint_details",

                    complaint_id=complaint.id

                )

            )

    return render_template(

        "admin/assign_complaint.html",

        form=form,

        complaint=complaint

    )


# ==========================================================
# UPDATE COMPLAINT
# ==========================================================

@admin.route(
    "/admin/update/<int:complaint_id>",
    methods=["GET", "POST"]
)
@admin_required
def update_complaint(complaint_id):

    complaint = AdminUpdateService.get_complaint(
        complaint_id
    )

    if complaint is None:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for("admin.complaints")
        )

    form = UpdateComplaintForm()

    if request.method == "GET":

        form.status.data = complaint.status

        form.resolution.data = complaint.resolution

    if form.validate_on_submit():

        AdminUpdateService.update_complaint(

            complaint_id=complaint.id,

            form=form,

            admin_id=session["user_id"]

        )

        flash(

            "Complaint updated successfully.",

            "success"

        )

        return redirect(

            url_for(

                "admin.complaint_details",

                complaint_id=complaint.id

            )

        )

    return render_template(

        "admin/update_complaint.html",

        form=form,

        complaint=complaint

    )
    
    # ==========================================================
# REPORTS
# ==========================================================

@admin.route("/admin/reports")
@admin_required
def reports():

    return render_template(

        "admin/reports.html",

        monthly=AdminService.monthly_statistics(),

        priority=AdminService.complaints_by_priority(),

        status=AdminService.complaints_by_status()

    )


# ==========================================================
# STAFF PERFORMANCE
# ==========================================================

@admin.route("/admin/performance")
@admin_required
def performance():

    statistics = PerformanceService.staff_statistics()

    return render_template(

        "admin/performance.html",

        statistics=statistics

    )