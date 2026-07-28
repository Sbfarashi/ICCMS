from constants.roles import UserRole

from models.user import User
from models.complaint import Complaint


class PerformanceService:
    """
    Service for staff performance statistics.
    """

    @staticmethod
    def staff_statistics():

        staff_members = (

            User.query

            .filter(

                User.role.in_(

                    UserRole.STAFF_ROLES

                )

            )

            .filter(

                User.is_active == True

            )

            .order_by(

                User.full_name.asc()

            )

            .all()

        )

        statistics = []

        for staff in staff_members:

            assigned = Complaint.query.filter_by(

                assigned_to=staff.id

            ).count()

            pending = Complaint.query.filter_by(

                assigned_to=staff.id,

                status="Pending"

            ).count()

            assigned_status = Complaint.query.filter_by(

                assigned_to=staff.id,

                status="Assigned"

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

            open_cases = (

                pending +

                assigned_status +

                in_progress

            )

            completion_rate = 0

            if assigned > 0:

                completion_rate = round(

                    ((resolved + closed) / assigned) * 100,

                    2

                )

            statistics.append({

                "staff": staff,

                "assigned": assigned,

                "pending": pending,

                "assigned_status": assigned_status,

                "in_progress": in_progress,

                "resolved": resolved,

                "closed": closed,

                "open_cases": open_cases,

                "completion_rate": completion_rate

            })

        statistics.sort(

            key=lambda item: (

                item["completion_rate"],

                item["resolved"],

                item["closed"]

            ),

            reverse=True

        )

        return statistics