from datetime import datetime

from sqlalchemy import func, or_, case

from extensions import db

from models.user import User
from models.category import Category
from models.complaint import Complaint
from models.complaint_history import ComplaintHistory

from constants.roles import UserRole


class StaffService:

    # ==========================================================
    # DASHBOARD STATISTICS
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
    # MY DASHBOARD
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

        return Complaint.query.order_by(

            Complaint.created_at.desc()

        ).limit(limit).all()

    # ==========================================================
    # MY ASSIGNED COMPLAINTS
    # ==========================================================

    @staticmethod
    def my_assigned_complaints(user_id, limit=10):

        return Complaint.query.filter(

            Complaint.assigned_to == user_id

        ).order_by(

            Complaint.created_at.desc()

        ).limit(limit).all()

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

        query = Complaint.query.filter(

            Complaint.assigned_to == user_id

        ).join(

            User,

            Complaint.customer_id == User.id

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

        # ===========================================
        # SORTING
        # ===========================================

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

        query = Complaint.query.join(

            User,

            Complaint.customer_id == User.id

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

        return query.order_by(

            Complaint.created_at.desc()

        ).all()

    # ==========================================================
    # GET SINGLE COMPLAINT
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

        return ComplaintHistory.query.filter_by(

            complaint_id=complaint_id

        ).order_by(

            ComplaintHistory.created_at.desc()

        ).all()

    # ==========================================================
    # GET STAFF USERS
    # ==========================================================

    @staticmethod
    def get_staff_users():

        return User.query.filter(

            User.role.in_(

                [

                    UserRole.STAFF,

                    UserRole.ENGINEER,

                    UserRole.SUPERVISOR

                ]

            )

        ).order_by(

            User.full_name.asc()

        ).all()

    # ==========================================================
    # ASSIGN COMPLAINT
    # ==========================================================

    @staticmethod
    def assign_complaint(

        complaint_id,

        staff_id,

        performed_by

    ):

        complaint = Complaint.query.get_or_404(

            complaint_id

        )

        previous_status = complaint.status

        complaint.assigned_to = staff_id

        complaint.status = "Assigned"

        complaint.assigned_at = datetime.utcnow()

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint.id,

                action="Complaint Assigned",

                previous_status=previous_status,

                new_status="Assigned",

                remarks="Complaint assigned to staff.",

                performed_by=performed_by

            )

        )

        db.session.commit()

        return complaint

    # ==========================================================
    # UPDATE STATUS
    # ==========================================================

    @staticmethod
    def update_status(

        complaint_id,

        status,

        performed_by

    ):

        complaint = Complaint.query.get_or_404(

            complaint_id

        )

        previous_status = complaint.status

        complaint.status = status

        if status == "Closed":

            complaint.closed_at = datetime.utcnow()

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint.id,

                action="Status Updated",

                previous_status=previous_status,

                new_status=status,

                remarks=f"Status changed to {status}.",

                performed_by=performed_by

            )

        )

        db.session.commit()

        return complaint

    # ==========================================================
    # ADD RESOLUTION
    # ==========================================================

    @staticmethod
    def add_resolution(

        complaint_id,

        resolution,

        performed_by

    ):

        complaint = Complaint.query.get_or_404(

            complaint_id

        )

        previous_status = complaint.status

        complaint.resolution = resolution

        complaint.status = "Resolved"

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint.id,

                action="Complaint Resolved",

                previous_status=previous_status,

                new_status="Resolved",

                remarks=resolution,

                performed_by=performed_by

            )

        )

        db.session.commit()

        return complaint

    # ==========================================================
    # STAFF WORKLOAD
    # ==========================================================

    @staticmethod
    def staff_workload():

        return (

            db.session.query(

                User,

                func.count(Complaint.id).label("total")

            )

            .outerjoin(

                Complaint,

                User.id == Complaint.assigned_to

            )

            .filter(

                User.role.in_(

                    [

                        UserRole.STAFF,

                        UserRole.ENGINEER,

                        UserRole.SUPERVISOR

                    ]

                )

            )

            .group_by(

                User.id

            )

            .order_by(

                User.full_name.asc()

            )

            .all()

        )
            # ==========================================================
    # GET USER PROFILE
    # ==========================================================

    @staticmethod
    def get_user(user_id):

        return User.query.get_or_404(user_id)


    # ==========================================================
    # UPDATE USER PROFILE
    # ==========================================================

    @staticmethod
    def update_profile(
        user_id,
        full_name,
        email,
        phone
    ):

        user = User.query.get_or_404(user_id)

        user.full_name = full_name
        user.email = email
        user.phone = phone

        db.session.commit()

        return user


    # ==========================================================
    # CHANGE PASSWORD
    # ==========================================================

    @staticmethod
    def change_password(
        user_id,
        password_hash
    ):

        user = User.query.get_or_404(user_id)

        user.password = password_hash

        db.session.commit()

        return user