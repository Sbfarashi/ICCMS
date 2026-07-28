from extensions import db, bcrypt

from models.user import User
from models.category import Category
from models.department import Department
from models.priority import Priority
from models.complaint_status import ComplaintStatus

from constants.roles import UserRole


class BootstrapService:

    @staticmethod
    def bootstrap():
        """
        Seeds all default system data.

        Safe to execute multiple times.
        """

        BootstrapService.seed_departments()
        BootstrapService.seed_categories()
        BootstrapService.seed_priorities()
        BootstrapService.seed_statuses()
        BootstrapService.seed_admin()

        db.session.commit()

        print("Bootstrap completed successfully.")

    # ==========================================================
    # Departments
    # ==========================================================

    @staticmethod
    def seed_departments():

        departments = [
            "ICT",
            "Customer Care",
            "Technical",
            "Engineering",
            "Installation",
            "Quality Assurance",
            "Finance",
            "Stores",
            "Management"
        ]

        for name in departments:

            exists = Department.query.filter_by(
                name=name
            ).first()

            if not exists:

                db.session.add(
                    Department(name=name)
                )

    # ==========================================================
    # Complaint Categories
    # ==========================================================

    @staticmethod
    def seed_categories():

        categories = [
            "Billing",
            "Meter Fault",
            "Power Outage",
            "Installation",
            "Voltage Fluctuation",
            "Token Issue",
            "Meter Replacement",
            "Network Issue",
            "General Complaint"
        ]

        for name in categories:

            exists = Category.query.filter_by(
                name=name
            ).first()

            if not exists:

                db.session.add(
                    Category(name=name)
                )

    # ==========================================================
    # Complaint Priorities
    # ==========================================================

    @staticmethod
    def seed_priorities():

        priorities = [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

        for name in priorities:

            exists = Priority.query.filter_by(
                name=name
            ).first()

            if not exists:

                db.session.add(
                    Priority(name=name)
                )

    # ==========================================================
    # Complaint Statuses
    # ==========================================================

    @staticmethod
    def seed_statuses():

        statuses = [
            "Pending",
            "Assigned",
            "In Progress",
            "Resolved",
            "Closed",
            "Escalated",
            "Rejected"
        ]

        for name in statuses:

            exists = ComplaintStatus.query.filter_by(
                name=name
            ).first()

            if not exists:

                db.session.add(
                    ComplaintStatus(name=name)
                )

    # ==========================================================
    # Default Administrator
    # ==========================================================

    @staticmethod
    def seed_admin():

        admin = User.query.filter_by(
            email="admin@smartmeters.com"
        ).first()

        if admin:
            return

        password = bcrypt.generate_password_hash(
            "admin123"
        ).decode("utf-8")

        admin = User(
            full_name="System Administrator",
            email="admin@smartmeters.com",
            phone="08000000000",
            password=password,
            role=UserRole.ADMIN
        )

        db.session.add(admin)