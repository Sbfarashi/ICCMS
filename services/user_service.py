from sqlalchemy import or_

from extensions import db
from models.user import User
from models.complaint import Complaint


class AdminUserService:

    @staticmethod
    def all_users():

        return (

            User.query

            .order_by(User.full_name)

            .all()

        )

    @staticmethod
    def search(keyword):

        if not keyword:

            return AdminUserService.all_users()

        return (

            User.query

            .filter(

                or_(

                    User.full_name.ilike(f"%{keyword}%"),

                    User.email.ilike(f"%{keyword}%"),

                    User.phone.ilike(f"%{keyword}%"),

                    User.role.ilike(f"%{keyword}%")

                )

            )

            .order_by(User.full_name)

            .all()

        )

    @staticmethod
    def get_user(user_id):

        return User.query.get(user_id)

    @staticmethod
    def complaints(user_id):

        return (

            Complaint.query

            .filter_by(customer_id=user_id)

            .order_by(Complaint.created_at.desc())

            .all()

        )

    @staticmethod
    def delete_user(user):

        db.session.delete(user)

        db.session.commit()

    @staticmethod
    def toggle_status(user):

        # This assumes your User model has an 'is_active' field.
        # If it does not, we'll add it later.

        user.is_active = not user.is_active

        db.session.commit()

    @staticmethod
    def total_users():

        return User.query.count()

    @staticmethod
    def total_customers():

        return User.query.filter_by(

            role="customer"

        ).count()

    @staticmethod
    def total_staff():

        return User.query.filter(

            User.role.in_(

                ["staff", "engineer"]

            )

        ).count()