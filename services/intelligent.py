from models.category import Category
from models.complaint import Complaint


class IntelligentEngine:

    # ==========================================
    # Detect Category
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
                "electricity"
            ],

            "Meter Fault": [
                "meter",
                "display",
                "fault",
                "damaged",
                "burnt",
                "error",
                "blank screen"
            ],

            "Token Issues": [
                "token",
                "recharge",
                "credit",
                "units",
                "rejected token"
            ],

            "Installation": [
                "install",
                "installation",
                "replace",
                "replacement"
            ],

            "Billing": [
                "billing",
                "bill",
                "charged",
                "overcharged",
                "undercharged"
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

        return None

    # ==========================================
    # Assign Priority
    # ==========================================

    @staticmethod
    def assign_priority(description):

        text = description.lower()

        critical = [
            "fire",
            "explosion",
            "electric shock",
            "life",
            "danger",
            "sparking"
        ]

        high = [
            "burnt",
            "smoke",
            "outage",
            "blackout",
            "transformer"
        ]

        medium = [
            "meter",
            "display",
            "token",
            "recharge",
            "billing"
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
    def is_duplicate(customer_id, title):

        complaint = Complaint.query.filter_by(
            customer_id=customer_id,
            title=title
        ).first()

        if complaint:
            return True

        return False