from flask import Blueprint
from flask import render_template

from decorators.auth import login_required
from services.report_service import ReportService


report = Blueprint(
    "report",
    __name__,
    url_prefix="/reports"
)


# =====================================================
# REPORTS DASHBOARD
# =====================================================

@report.route("/")
@login_required
def dashboard():

    totals = ReportService.totals()

    status = ReportService.complaints_by_status()

    priority = ReportService.complaints_by_priority()

    category = ReportService.complaints_by_category()

    monthly = ReportService.monthly_statistics()

    recent = ReportService.recent_complaints()

    closed = ReportService.recently_closed()

    workload = ReportService.staff_workload()

    return render_template(

        "reports/dashboard.html",

        totals=totals,

        status=status,

        priority=priority,

        category=category,

        monthly=monthly,

        recent=recent,

        closed=closed,

        workload=workload

    )