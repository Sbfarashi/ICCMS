from datetime import datetime

from extensions import db

from models.complaint import Complaint
from services.history_service import HistoryService


class EscalationService:
    """
    Intelligent SLA-Based Complaint Escalation Service.
    """

    # =====================================================
    # Escalation Rules (Hours)
    # =====================================================

    ESCALATION_RULES = {

        "Critical": {
            1: 12,
            2: 24,
            3: 48
        },

        "High": {
            1: 24,
            2: 48,
            3: 72
        },

        "Medium": {
            1: 48,
            2: 72,
            3: 96
        },

        "Low": {
            1: 72,
            2: 96,
            3: 120
        }

    }

    # =====================================================
    # Run Escalation
    # =====================================================

    @staticmethod
    def run():

        now = datetime.utcnow()

        complaints = Complaint.query.filter(

            Complaint.status.notin_(
                [
                    "Resolved",
                    "Closed"
                ]
            )

        ).all()

        updated = 0

        for complaint in complaints:

            level = EscalationService.calculate_level(
                complaint,
                now
            )

            if level != complaint.escalation_level:

                previous = complaint.escalation_level

                complaint.escalation_level = level

                HistoryService.log(

                    complaint_id=complaint.id,

                    action="Automatic Escalation",

                    previous_status=f"Level {previous}",

                    new_status=f"Level {level}",

                    remarks=(
                        f"Automatically escalated "
                        f"based on "
                        f"{complaint.priority} priority SLA."
                    ),

                    performed_by=None

                )

                updated += 1

        db.session.commit()

        return updated

    # =====================================================
    # Calculate Escalation Level
    # =====================================================

    @staticmethod
    def calculate_level(complaint, current_time):

        elapsed_hours = (

            current_time - complaint.created_at

        ).total_seconds() / 3600

        rules = EscalationService.ESCALATION_RULES.get(

            complaint.priority,

            EscalationService.ESCALATION_RULES["Medium"]

        )

        if elapsed_hours >= rules[3]:

            return 3

        if elapsed_hours >= rules[2]:

            return 2

        if elapsed_hours >= rules[1]:

            return 1

        return 0

    # =====================================================
    # Dashboard Statistics
    # =====================================================

    @staticmethod
    def statistics():

        return {

            "level1": Complaint.query.filter_by(
                escalation_level=1
            ).count(),

            "level2": Complaint.query.filter_by(
                escalation_level=2
            ).count(),

            "level3": Complaint.query.filter_by(
                escalation_level=3
            ).count(),

            "total": Complaint.query.filter(
                Complaint.escalation_level > 0
            ).count()

        }

    # =====================================================
    # Escalated Complaints
    # =====================================================

    @staticmethod
    def escalated():

        return (

            Complaint.query

            .filter(
                Complaint.escalation_level > 0
            )

            .order_by(
                Complaint.escalation_level.desc(),
                Complaint.created_at.asc()
            )

            .all()

        )