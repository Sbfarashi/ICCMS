from flask import current_app

from extensions import db
from extensions import bcrypt

from models.user import User
from constants.roles import UserRole


class BootstrapService:

    @staticmethod
    def create_user(name, email, phone, password, role):

        user = User.query.filter_by(email=email).first()

        if user:
            return

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        user = User(
            full_name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            role=role,
            is_active=True
        )

        db.session.add(user)
        db.session.commit()

        print(f"✔ {role.capitalize()} account created.")

    @staticmethod
    def bootstrap():

        BootstrapService.create_user(
            name="System Administrator",
            email="admin@smartmeters.com",
            phone="08000000001",
            password="admin123",
            role=UserRole.ADMIN
        )

        BootstrapService.create_user(
            name="Complaint Staff",
            email="staff@smartmeters.com",
            phone="08000000002",
            password="staff123",
            role=UserRole.STAFF
        )

        BootstrapService.create_user(
            name="Complaint Engineer",
            email="engineer@smartmeters.com",
            phone="08000000003",
            password="engineer123",
            role=UserRole.ENGINEER
        )

        BootstrapService.create_user(
            name="Complaint Supervisor",
            email="supervisor@smartmeters.com",
            phone="08000000004",
            password="supervisor123",
            role=UserRole.SUPERVISOR
        )