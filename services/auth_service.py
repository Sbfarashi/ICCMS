from datetime import datetime

from flask import session

from extensions import db
from extensions import bcrypt

from models.user import User
from constants.roles import UserRole


class AuthService:

    # ===================================================
    # REGISTER USER
    # ===================================================

    @staticmethod
    def register(form):

        try:

            existing_email = User.query.filter_by(
                email=form.email.data.strip().lower()
            ).first()

            if existing_email:
                return False, "Email address already exists."

            existing_phone = User.query.filter_by(
                phone=form.phone.data.strip()
            ).first()

            if existing_phone:
                return False, "Phone number already exists."

            hashed_password = bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")

            user = User(
                full_name=form.full_name.data.strip(),
                email=form.email.data.strip().lower(),
                phone=form.phone.data.strip(),
                password=hashed_password,
                role=form.role.data
            )

            db.session.add(user)
            db.session.commit()

            return True, "Registration completed successfully."

        except Exception as e:

            db.session.rollback()

            return False, f"Registration failed: {str(e)}"

    # ===================================================
    # LOGIN USER
    # ===================================================

    @staticmethod
    def login(form):

        try:

            email = form.email.data.strip().lower()
            password = form.password.data

            user = User.query.filter_by(
                email=email
            ).first()

            if user is None:
                return False, "Invalid email or password.", None

            if not bcrypt.check_password_hash(
                user.password,
                password
            ):
                return False, "Invalid email or password.", None

            if not user.is_active:
                return False, "Your account has been deactivated.", None

            session.clear()

            session["user_id"] = user.id
            session["user_name"] = user.full_name
            session["full_name"] = user.full_name
            session["email"] = user.email
            session["role"] = user.role
            session["logged_in"] = True

            user.last_login = datetime.utcnow()

            db.session.commit()

            return (
                True,
                f"Welcome back, {user.full_name}.",
                user.role
            )

        except Exception as e:

            db.session.rollback()

            return (
                False,
                f"Login failed: {str(e)}",
                None
            )

    # ===================================================
    # CHANGE PASSWORD
    # ===================================================

    @staticmethod
    def change_password(user_id, form):

        try:

            user = User.query.filter_by(
                id=user_id
            ).first()

            if user is None:
                return False, "User not found."

            if not bcrypt.check_password_hash(
                user.password,
                form.current_password.data
            ):
                return False, "Current password is incorrect."

            if form.current_password.data == form.new_password.data:
                return (
                    False,
                    "New password must be different from the current password."
                )

            user.password = bcrypt.generate_password_hash(
                form.new_password.data
            ).decode("utf-8")

            db.session.commit()

            return True, "Password changed successfully."

        except Exception as e:

            db.session.rollback()

            return False, f"Password change failed: {str(e)}"

    # ===================================================
    # LOGOUT USER
    # ===================================================

    @staticmethod
    def logout():

        session.clear()

        return True