from flask import request

from extensions import db
from models.activity_log import ActivityLog


class ActivityLogService:
    """
    Service for recording and retrieving user activities.
    """

    @staticmethod
    def log(user_id, activity, module):
        """
        Record a new activity.
        """

        log = ActivityLog(
            user_id=user_id,
            activity=activity,
            module=module,
            ip_address=request.remote_addr
        )

        db.session.add(log)
        db.session.commit()

    @staticmethod
    def get_user_logs(user_id):
        """
        Retrieve all activities performed by a specific user.
        """

        return (
            ActivityLog.query
            .filter_by(user_id=user_id)
            .order_by(ActivityLog.created_at.desc())
            .all()
        )

    @staticmethod
    def get_all_logs():
        """
        Retrieve all activities in the system.
        """

        return (
            ActivityLog.query
            .order_by(ActivityLog.created_at.desc())
            .all()
        )

    @staticmethod
    def delete_log(log_id):
        """
        Delete a specific activity log.
        """

        log = ActivityLog.query.get(log_id)

        if log:
            db.session.delete(log)
            db.session.commit()

    @staticmethod
    def clear_logs():
        """
        Delete all activity logs.
        """

        ActivityLog.query.delete()
        db.session.commit()