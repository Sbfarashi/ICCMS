from sqlalchemy import func

from models.user import User
from models.complaint import Complaint
from models.category import Category
from services.escalation_service import EscalationService


class AdminService:

    # =====================================================
    # Dashboard
    # =====================================================

    @staticmethod
    def dashboard():

        total_users = User.query.filter_by(
            role="customer"
        ).count()

        total_staff = User.query.filter_by(
            role="staff"
        ).count()

        total_complaints = Complaint.query.count()

        pending = Complaint.query.filter_by(
            status="Pending"
        ).count()

        in_progress = Complaint.query.filter_by(
            status="In Progress"
        ).count()

        resolved = Complaint.query.filter_by(
            status="Resolved"
        ).count()

        closed = Complaint.query.filter_by(
            status="Closed"
        ).count()

        recent = (

            Complaint.query

            .order_by(
                Complaint.created_at.desc()
            )

            .limit(10)

            .all()

        )

        escalation = EscalationService.statistics()

        escalated = EscalationService.escalated()[:5]

        return {

            "total_users": total_users,

            "total_staff": total_staff,

            "total_complaints": total_complaints,

            "pending": pending,

            "in_progress": in_progress,

            "resolved": resolved,

            "closed": closed,

            "recent": recent,

            "escalation": escalation,

            "recent_escalated": escalated

        }

    # =====================================================
    # Monthly Statistics
    # =====================================================

    @staticmethod
    def monthly_statistics():

        return (

            Complaint.query

            .with_entities(

                func.strftime(
                    "%Y-%m",
                    Complaint.created_at
                ).label("month"),

                func.count().label("total")

            )

            .group_by("month")

            .order_by("month")

            .all()

        )

    # =====================================================
    # Priority Statistics
    # =====================================================

    @staticmethod
    def complaints_by_priority():

        return (

            Complaint.query

            .with_entities(

                Complaint.priority,

                func.count().label("total")

            )

            .group_by(
                Complaint.priority
            )

            .all()

        )

    # =====================================================
    # Status Statistics
    # =====================================================

    @staticmethod
    def complaints_by_status():

        return (

            Complaint.query

            .with_entities(

                Complaint.status,

                func.count().label("total")

            )

            .group_by(
                Complaint.status
            )

            .all()

        )

    # =====================================================
    # Staff Workload
    # =====================================================

    @staticmethod
    def staff_workload():

        return (

            User.query

            .filter_by(role="staff")

            .all()

        )