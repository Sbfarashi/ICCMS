from datetime import datetime

from models.complaint import Complaint
from models.user import User
from models.category import Category


class SearchService:
    """
    Handles advanced complaint searching and filtering.
    """

    @staticmethod
    def search(filters):

        query = Complaint.query

        # ==========================================
        # Complaint Number
        # ==========================================

        complaint_number = filters.get("complaint_number")

        if complaint_number:

            query = query.filter(
                Complaint.complaint_number.ilike(
                    f"%{complaint_number}%"
                )
            )

        # ==========================================
        # Meter Number
        # ==========================================

        meter_number = filters.get("meter_number")

        if meter_number:

            query = query.filter(
                Complaint.meter_number.ilike(
                    f"%{meter_number}%"
                )
            )

        # ==========================================
        # Customer Name
        # ==========================================

        customer = filters.get("customer")

        if customer:

            query = (
                query
                .join(Complaint.customer)
                .filter(
                    User.full_name.ilike(
                        f"%{customer}%"
                    )
                )
            )

        # ==========================================
        # Status
        # ==========================================

        status = filters.get("status")

        if status:

            query = query.filter(
                Complaint.status == status
            )

        # ==========================================
        # Priority
        # ==========================================

        priority = filters.get("priority")

        if priority:

            query = query.filter(
                Complaint.priority == priority
            )

        # ==========================================
        # Category
        # ==========================================

        category = filters.get("category")

        if category:

            query = (
                query
                .join(Complaint.category)
                .filter(
                    Category.name == category
                )
            )

        # ==========================================
        # Date From
        # ==========================================

        date_from = filters.get("date_from")

        if date_from:

            try:

                start_date = datetime.strptime(
                    date_from,
                    "%Y-%m-%d"
                )

                query = query.filter(
                    Complaint.created_at >= start_date
                )

            except ValueError:
                pass

        # ==========================================
        # Date To
        # ==========================================

        date_to = filters.get("date_to")

        if date_to:

            try:

                end_date = datetime.strptime(
                    date_to,
                    "%Y-%m-%d"
                )

                # Include the entire selected day
                end_date = end_date.replace(
                    hour=23,
                    minute=59,
                    second=59
                )

                query = query.filter(
                    Complaint.created_at <= end_date
                )

            except ValueError:
                pass

        # ==========================================
        # Sort Results
        # ==========================================

        query = query.order_by(
            Complaint.created_at.desc()
        )

        return query