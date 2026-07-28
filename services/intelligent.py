from datetime import datetime, timedelta

from extensions import db
from models.category import Category
from models.complaint import Complaint


class IntelligentEngine:

    # ==========================================
    # Automatic Category Detection
    # ==========================================

    @staticmethod
    def detect_category(description):

        text = description.lower()

        rules = {

            "Power Supply": [
                "no light",
                "blackout",
                "outage",
                "power failure",
                "power outage",
                "electricity",
                "transformer"
            ],

            "Meter Fault": [
                "meter",
                "display",
                "fault",
                "damaged",
                "burnt",
                "blank",
                "error"
            ],

            "Token Issues": [
                "token",
                "recharge",
                "credit",
                "units",
                "voucher",
                "token rejected"
            ],

            "Billing": [
                "bill",
                "billing",
                "overcharged",
                "undercharged",
                "estimated bill"
            ],

            "Installation": [
                "installation",
                "install",
                "replace",
                "replacement",
                "seal"
            ],

            "Tampering": [
                "tamper",
                "illegal connection",
                "bypass",
                "stolen meter"
            ]

        }

        for category_name, keywords in rules.items():

            for keyword in keywords:

                if keyword in text:

                    category = Category.query.filter_by(
                        name=category_name
                    ).first()

                    if category:

                        return category.id

        category = Category.query.filter_by(
            name="General"
        ).first()

        if category:

            return category.id

        return None

    # ==========================================
    # Automatic Priority
    # ==========================================

    @staticmethod
    def assign_priority(description):

        text = description.lower()

        critical = [
            "fire",
            "explosion",
            "electric shock",
            "danger",
            "life",
            "sparking"
        ]

        high = [
            "burnt",
            "smoke",
            "blackout",
            "power outage",
            "transformer"
        ]

        medium = [
            "meter",
            "display",
            "fault",
            "token",
            "billing",
            "installation"
        ]

        for word in critical:

            if word in text:

                return "Critical"

        for word in high:

            if word in text:

                return "High"

        for word in medium:

            if word in text:

                return "Medium"

        return "Low"

    # ==========================================
    # Duplicate Detection
    # ==========================================

    @staticmethod
    def is_duplicate(
        customer_id,
        meter_number,
        description
    ):

        complaints = Complaint.query.filter(

            Complaint.customer_id == customer_id,

            Complaint.meter_number == meter_number,

            Complaint.status.in_(

                [

                    "Pending",

                    "Assigned",

                    "In Progress",

                    "Escalated"

                ]

            )

        ).all()

        description = description.lower()

        for complaint in complaints:

            score = 0

            previous = complaint.description.lower()

            for word in description.split():

                if word in previous:

                    score += 1

            if score >= 3:

                return True

        return False

    # ==========================================
    # Automatic Escalation
    # ==========================================

    @staticmethod
    def auto_escalate():

        limit = datetime.utcnow() - timedelta(hours=48)

        complaints = Complaint.query.filter(

            Complaint.status.in_(

                [

                    "Pending",

                    "Assigned",

                    "In Progress"

                ]

            ),

            Complaint.created_at <= limit

        ).all()

        updated = 0

        for complaint in complaints:

            complaint.status = "Escalated"

            complaint.escalation_level += 1

            updated += 1

        db.session.commit()

        return updated