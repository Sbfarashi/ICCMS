from sqlalchemy import or_

from extensions import db

from models.user import User
from models.complaint import Complaint

from constants.roles import UserRole


class AdminUserService:

    # =====================================================
    # Dashboard Statistics
    # =====================================================

    @staticmethod
    def total_users():

        return User.query.count()

    @staticmethod
    def total_customers():

        return User.query.filter_by(
            role=UserRole.CUSTOMER
        ).count()

    @staticmethod
    def total_staff():

        return User.query.filter(
            User.role.in_(
                [
                    UserRole.STAFF,
                    UserRole.ENGINEER,
                    UserRole.ADMIN
                ]
            )
        ).count()

    # =====================================================
    # Users
    # =====================================================

    @staticmethod
    def get_all_users():

        return (
            User.query
            .order_by(User.full_name.asc())
            .all()
        )

    @staticmethod
    def get_user(user_id):

        return User.query.get_or_404(user_id)

    # =====================================================
    # Search Users
    # =====================================================

    @staticmethod
    def search(keyword):

        if not keyword:

            return AdminUserService.get_all_users()

        return (
            User.query
            .filter(
                or_(
                    User.full_name.ilike(f"%{keyword}%"),
                    User.email.ilike(f"%{keyword}%"),
                    User.phone.ilike(f"%{keyword}%"),
                    User.employee_id.ilike(f"%{keyword}%"),
                    User.role.ilike(f"%{keyword}%")
                )
            )
            .order_by(User.full_name.asc())
            .all()
        )

    # =====================================================
    # Customer Complaint History
    # =====================================================

    @staticmethod
    def complaints(user_id):

        return (
            Complaint.query
            .filter_by(customer_id=user_id)
            .order_by(Complaint.created_at.desc())
            .all()
        )

    # =====================================================
    # Activate User
    # =====================================================

    @staticmethod
    def activate(user):

        user.is_active = True

        db.session.commit()

        return user

    # =====================================================
    # Deactivate User
    # =====================================================

    @staticmethod
    def deactivate(user):

        user.is_active = False

        db.session.commit()

        return user

    # =====================================================
    # Toggle User Status
    # =====================================================

    @staticmethod
    def toggle_status(user):

        user.is_active = not user.is_active

        db.session.commit()

        return user

    # =====================================================
    # Update User
    # =====================================================

    @staticmethod
    def update_user(user, form):

        user.full_name = form.full_name.data
        user.employee_id = form.employee_id.data
        user.designation = form.designation.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.role = form.role.data
        user.department_id = form.department.data

        db.session.commit()

        return user

    # =====================================================
    # Create User
    # =====================================================

    @staticmethod
    def create_user(
        full_name,
        employee_id,
        designation,
        email,
        phone,
        password,
        role,
        department_id
    ):

        user = User(
            full_name=full_name,
            employee_id=employee_id,
            designation=designation,
            email=email,
            phone=phone,
            password=password,
            role=role,
            department_id=department_id
        )

        db.session.add(user)
        db.session.commit()

        return user

    # =====================================================
    # Delete User
    # =====================================================

    @staticmethod
    def delete_user(user):

        db.session.delete(user)

        db.session.commit()

        return True