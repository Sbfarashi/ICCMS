from sqlalchemy import func

from extensions import db

from constants.roles import UserRole

from models.complaint import Complaint
from models.user import User
from models.category import Category


class ReportService:

    # =====================================================
    # DASHBOARD TOTALS
    # =====================================================

    @staticmethod
    def totals():

        return {

            "complaints": Complaint.query.count(),

            "customers": User.query.filter_by(
                role=UserRole.CUSTOMER
            ).count(),

            "staff": User.query.filter(

                User.role.in_(

                    UserRole.STAFF_ROLES + [
                        UserRole.ADMIN
                    ]

                )

            ).count(),

            "categories": Category.query.count()

        }

    # =====================================================
    # COMPLAINTS BY STATUS
    # =====================================================

    @staticmethod
    def complaints_by_status():

        results = (

            db.session.query(

                Complaint.status,

                func.count(
                    Complaint.id
                )

            )

            .group_by(
                Complaint.status
            )

            .order_by(
                Complaint.status
            )

            .all()

        )

        return [

            {
                "status": status,
                "count": total
            }

            for status, total in results

        ]

    # =====================================================
    # COMPLAINTS BY PRIORITY
    # =====================================================

    @staticmethod
    def complaints_by_priority():

        results = (

            db.session.query(

                Complaint.priority,

                func.count(
                    Complaint.id
                )

            )

            .group_by(
                Complaint.priority
            )

            .order_by(
                Complaint.priority
            )

            .all()

        )

        return [

            {
                "priority": priority,
                "count": total
            }

            for priority, total in results

        ]

    # =====================================================
    # COMPLAINTS BY CATEGORY
    # =====================================================

    @staticmethod
    def complaints_by_category():

        results = (

            db.session.query(

                Category.name,

                func.count(
                    Complaint.id
                )

            )

            .join(
                Complaint.category
            )

            .group_by(
                Category.name
            )

            .order_by(
                Category.name
            )

            .all()

        )

        return [

            {
                "category": name,
                "count": total
            }

            for name, total in results

        ]

    # =====================================================
    # MONTHLY STATISTICS
    # =====================================================

    @staticmethod
    def monthly_statistics():

        results = (

            db.session.query(

                func.strftime(

                    "%Y-%m",

                    Complaint.created_at

                ).label("month"),

                func.count(

                    Complaint.id

                ).label("total")

            )

            .group_by(

                func.strftime(

                    "%Y-%m",

                    Complaint.created_at

                )

            )

            .order_by(

                func.strftime(

                    "%Y-%m",

                    Complaint.created_at

                )

            )

            .all()

        )

        return [

            {
                "month": month,
                "total": total
            }

            for month, total in results

        ]

    # =====================================================
    # RECENT COMPLAINTS
    # =====================================================

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

    # =====================================================
    # RECENTLY CLOSED COMPLAINTS
    # =====================================================

    @staticmethod
    def recently_closed(limit=10):

        return (

            Complaint.query

            .filter(

                Complaint.status == "Closed"

            )

            .order_by(

                Complaint.closed_at.desc()

            )

            .limit(limit)

            .all()

        )

    # =====================================================
    # STAFF WORKLOAD
    # =====================================================

    @staticmethod
    def staff_workload():

        results = (

            db.session.query(

                User.full_name,

                func.count(
                    Complaint.id
                )

            )

            .outerjoin(

                Complaint,

                Complaint.assigned_to == User.id

            )

            .filter(

                User.role.in_(

                    UserRole.STAFF_ROLES

                )

            )

            .group_by(

                User.full_name

            )

            .order_by(

                User.full_name

            )

            .all()

        )

        return [

            {
                "staff": name,
                "assigned": total
            }

            for name, total in results

        ]