from datetime import datetime

from sqlalchemy import func, or_, case

from extensions import db

from models.user import User
from models.complaint import Complaint
from models.complaint_history import ComplaintHistory

from constants.roles import UserRole

from services.history_service import HistoryService
from services.notification_service import NotificationService


class StaffService:

    # ==========================================================
    # SYSTEM DASHBOARD
    # ==========================================================

    @staticmethod
    def dashboard_statistics():

        return {

            "total": Complaint.query.count(),

            "pending": Complaint.query.filter_by(
                status="Pending"
            ).count(),

            "assigned": Complaint.query.filter_by(
                status="Assigned"
            ).count(),

            "in_progress": Complaint.query.filter_by(
                status="In Progress"
            ).count(),

            "resolved": Complaint.query.filter_by(
                status="Resolved"
            ).count(),

            "closed": Complaint.query.filter_by(
                status="Closed"
            ).count()

        }

    # ==========================================================
    # STAFF DASHBOARD
    # ==========================================================

    @staticmethod
    def my_dashboard_statistics(user_id):

        return {

            "assigned": Complaint.query.filter_by(
                assigned_to=user_id
            ).count(),

            "pending": Complaint.query.filter_by(
                assigned_to=user_id,
                status="Pending"
            ).count(),

            "in_progress": Complaint.query.filter_by(
                assigned_to=user_id,
                status="In Progress"
            ).count(),

            "resolved": Complaint.query.filter_by(
                assigned_to=user_id,
                status="Resolved"
            ).count(),

            "closed": Complaint.query.filter_by(
                assigned_to=user_id,
                status="Closed"
            ).count()

        }

    # ==========================================================
    # RECENT COMPLAINTS
    # ==========================================================

    @staticmethod
    def recent_complaints(limit=10):

        return (

            Complaint.query

            .order_by(
                Complaint.created_at.desc()
            )

            .limit(limit)

            .all()

        )

    # ==========================================================
    # MY ASSIGNED COMPLAINTS
    # ==========================================================

    @staticmethod
    def my_assigned_complaints(user_id, limit=10):

        return (

            Complaint.query

            .filter(
                Complaint.assigned_to == user_id
            )

            .order_by(
                Complaint.created_at.desc()
            )

            .limit(limit)

            .all()

        )

    # ==========================================================
    # SEARCH MY COMPLAINTS
    # ==========================================================

    @staticmethod
    def search_my_complaints(

        user_id,
        search="",
        status="",
        priority="",
        sort="newest",
        page=1,
        per_page=10

    ):

        query = (

            Complaint.query

            .join(
                User,
                Complaint.customer_id == User.id
            )

            .filter(
                Complaint.assigned_to == user_id
            )

        )

        if search:

            keyword = f"%{search.strip()}%"

            query = query.filter(

                or_(

                    Complaint.complaint_number.ilike(keyword),

                    Complaint.title.ilike(keyword),

                    Complaint.meter_number.ilike(keyword),

                    User.full_name.ilike(keyword)

                )

            )

        if status:

            query = query.filter(
                Complaint.status == status
            )

        if priority:

            query = query.filter(
                Complaint.priority == priority
            )

        if sort == "oldest":

            query = query.order_by(
                Complaint.created_at.asc()
            )

        elif sort == "priority":

            priority_order = case(

                (Complaint.priority == "Critical", 1),

                (Complaint.priority == "High", 2),

                (Complaint.priority == "Medium", 3),

                (Complaint.priority == "Low", 4),

                else_=5

            )

            query = query.order_by(priority_order)

        elif sort == "status":

            query = query.order_by(
                Complaint.status.asc()
            )

        elif sort == "complaint":

            query = query.order_by(
                Complaint.complaint_number.asc()
            )

        else:

            query = query.order_by(
                Complaint.created_at.desc()
            )

        return query.paginate(

            page=page,

            per_page=per_page,

            error_out=False

        )

    # ==========================================================
    # SEARCH ALL COMPLAINTS
    # ==========================================================

    @staticmethod
    def search_complaints(

        search="",
        status="",
        priority=""

    ):

        query = (

            Complaint.query

            .join(
                User,
                Complaint.customer_id == User.id
            )

        )

        if search:

            keyword = f"%{search}%"

            query = query.filter(

                or_(

                    Complaint.complaint_number.ilike(keyword),

                    Complaint.title.ilike(keyword),

                    Complaint.meter_number.ilike(keyword),

                    User.full_name.ilike(keyword)

                )

            )

        if status:

            query = query.filter(
                Complaint.status == status
            )

        if priority:

            query = query.filter(
                Complaint.priority == priority
            )

        return (

            query

            .order_by(
                Complaint.created_at.desc()
            )

            .all()

        )

    # ==========================================================
    # GET COMPLAINT
    # ==========================================================

    @staticmethod
    def get_complaint(complaint_id):

        return Complaint.query.get_or_404(
            complaint_id
        )

    # ==========================================================
    # COMPLAINT HISTORY
    # ==========================================================

    @staticmethod
    def complaint_history(complaint_id):

        return (

            ComplaintHistory.query

            .filter_by(
                complaint_id=complaint_id
            )

            .order_by(
                ComplaintHistory.created_at.desc()
            )

            .all()

        )

    # ==========================================================
    # STAFF LIST
    # ==========================================================

    @staticmethod
    def get_staff_users():

        return (

            User.query

            .filter(

User.role.in_(
    UserRole.STAFF_ROLES
)

            )

            .order_by(
                User.full_name.asc()
            )

            .all()

        )
            # ==========================================================
    # ASSIGN COMPLAINT
    # ==========================================================

    @staticmethod
    def assign_complaint(
        complaint_id,
        staff_id,
        performed_by
    ):

        try:

            complaint = Complaint.query.get_or_404(
                complaint_id
            )

            staff = User.query.get_or_404(
                staff_id
            )

            previous_status = complaint.status

            complaint.assigned_to = staff.id
            complaint.assigned_at = datetime.utcnow()
            complaint.status = "Assigned"

            HistoryService.log(
                complaint_id=complaint.id,
                action="Complaint Assigned",
                previous_status=previous_status,
                new_status="Assigned",
                remarks=f"Complaint assigned to {staff.full_name}.",
                performed_by=performed_by
            )

            NotificationService.create(
                user_id=staff.id,
                title="New Complaint Assigned",
                message=(
                    f"Complaint "
                    f"{complaint.complaint_number} "
                    "has been assigned to you."
                ),
                notification_type="Assignment"
            )

            db.session.commit()

            return True, "Complaint assigned successfully."

        except Exception as e:

            db.session.rollback()

            return False, str(e)

    # ==========================================================
    # UPDATE COMPLAINT STATUS
    # ==========================================================

    @staticmethod
    def update_status(
        complaint_id,
        status,
        performed_by,
        remarks=""
    ):

        try:

            complaint = Complaint.query.get_or_404(
                complaint_id
            )

            previous_status = complaint.status

            complaint.status = status

            if status == "Closed":
                complaint.closed_at = datetime.utcnow()

            HistoryService.log(
                complaint_id=complaint.id,
                action="Status Updated",
                previous_status=previous_status,
                new_status=status,
                remarks=remarks if remarks else f"Status changed to {status}.",
                performed_by=performed_by
            )

            NotificationService.create(
                user_id=complaint.customer_id,
                title="Complaint Status Updated",
                message=(
                    f"Your complaint "
                    f"{complaint.complaint_number} "
                    f"is now {status}."
                ),
                notification_type="Status"
            )

            db.session.commit()

            return True, "Status updated successfully."

        except Exception as e:

            db.session.rollback()

            return False, str(e)

    # ==========================================================
    # ADD RESOLUTION
    # ==========================================================

    @staticmethod
    def add_resolution(
        complaint_id,
        resolution,
        performed_by
    ):

        try:

            complaint = Complaint.query.get_or_404(
                complaint_id
            )

            previous_status = complaint.status

            complaint.resolution = resolution
            complaint.status = "Resolved"

            # If your Complaint model has this field,
            # keep it. Otherwise remove the next line.
            if hasattr(complaint, "resolved_at"):
                complaint.resolved_at = datetime.utcnow()

            HistoryService.log(
                complaint_id=complaint.id,
                action="Complaint Resolved",
                previous_status=previous_status,
                new_status="Resolved",
                remarks=resolution,
                performed_by=performed_by
            )

            NotificationService.create(
                user_id=complaint.customer_id,
                title="Complaint Resolved",
                message=(
                    f"Your complaint "
                    f"{complaint.complaint_number} "
                    "has been resolved."
                ),
                notification_type="Resolution"
            )

            db.session.commit()

            return True, "Complaint resolved successfully."

        except Exception as e:

            db.session.rollback()

            return False, str(e)
            # ==========================================================
    # STAFF WORKLOAD
    # ==========================================================

    @staticmethod
    def staff_workload():

        return (

            db.session.query(

                User,

                func.count(
                    Complaint.id
                ).label("total")

            )

            .outerjoin(

                Complaint,

                User.id == Complaint.assigned_to

            )

            .filter(

User.role.in_(
    UserRole.STAFF_ROLES
)

            )

            .group_by(User.id)

            .order_by(
                User.full_name.asc()
            )

            .all()

        )

    # ==========================================================
    # GET USER
    # ==========================================================

    @staticmethod
    def get_user(user_id):

        return User.query.get_or_404(
            user_id
        )

    # ==========================================================
    # UPDATE PROFILE
    # ==========================================================

    @staticmethod
    def update_profile(

        user_id,
        full_name,
        email,
        phone

    ):

        try:

            user = User.query.get_or_404(
                user_id
            )

            user.full_name = full_name.strip()
            user.email = email.strip().lower()
            user.phone = phone.strip()

            db.session.commit()

            return (

                True,

                "Profile updated successfully."

            )

        except Exception as e:

            db.session.rollback()

            return (

                False,

                str(e)

            )

    # ==========================================================
    # CHANGE PASSWORD
    # ==========================================================

    @staticmethod
    def change_password(

        user_id,
        password_hash

    ):

        try:

            user = User.query.get_or_404(
                user_id
            )

            user.password = password_hash

            db.session.commit()

            return (

                True,

                "Password changed successfully."

            )

        except Exception as e:

            db.session.rollback()

            return (

                False,

                str(e)

            )

    # ==========================================================
    # GET COMPLAINT COUNTS
    # ==========================================================

    @staticmethod
    def complaint_summary():

        return {

            "total":

                Complaint.query.count(),

            "pending":

                Complaint.query.filter_by(
                    status="Pending"
                ).count(),

            "assigned":

                Complaint.query.filter_by(
                    status="Assigned"
                ).count(),

            "in_progress":

                Complaint.query.filter_by(
                    status="In Progress"
                ).count(),

            "resolved":

                Complaint.query.filter_by(
                    status="Resolved"
                ).count(),

            "closed":

                Complaint.query.filter_by(
                    status="Closed"
                ).count()

        }

    # ==========================================================
    # HIGH PRIORITY COMPLAINTS
    # ==========================================================

    @staticmethod
    def high_priority_complaints():

        return (

            Complaint.query

            .filter(

                Complaint.priority.in_(

                    [

                        "High",

                        "Critical"

                    ]

                )

            )

            .order_by(

                Complaint.created_at.desc()

            )

            .all()

        )

    # ==========================================================
    # OVERDUE COMPLAINTS
    # ==========================================================

    @staticmethod
    def overdue_complaints():

        return (

            Complaint.query

            .filter(

                Complaint.status.notin_(

                    [

                        "Resolved",

                        "Closed"

                    ]

                )

            )

            .order_by(

                Complaint.created_at.asc()

            )

            .all()

        )