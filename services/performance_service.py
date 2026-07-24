from sqlalchemy import func

from models.user import User
from models.complaint import Complaint


class PerformanceService:

    @staticmethod
    def staff_statistics():

        staff_members = User.query.filter_by(
            role="staff"
        ).all()

        statistics = []

        for staff in staff_members:

            assigned = Complaint.query.filter_by(
                assigned_to=staff.id
            ).count()

            pending = Complaint.query.filter_by(
                assigned_to=staff.id,
                status="Pending"
            ).count()

            in_progress = Complaint.query.filter_by(
                assigned_to=staff.id,
                status="In Progress"
            ).count()

            resolved = Complaint.query.filter_by(
                assigned_to=staff.id,
                status="Resolved"
            ).count()

            closed = Complaint.query.filter_by(
                assigned_to=staff.id,
                status="Closed"
            ).count()

            statistics.append({

                "staff": staff,

                "assigned": assigned,

                "pending": pending,

                "in_progress": in_progress,

                "resolved": resolved,

                "closed": closed

            })

        statistics.sort(

            key=lambda item: item["resolved"],

            reverse=True

        )

        return statistics