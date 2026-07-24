from models.database import db
from models.notification import Notification


class NotificationService:

    @staticmethod
    def create(user_id, title, message, notification_type="General"):

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )

        db.session.add(notification)
        db.session.commit()

        return notification


    @staticmethod
    def unread(user_id):

        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).all()


    @staticmethod
    def mark_as_read(notification_id):

        notification = Notification.query.get(notification_id)

        if notification:

            notification.is_read = True

            db.session.commit()

        return notification


    @staticmethod
    def all(user_id):

        return Notification.query.filter_by(
            user_id=user_id
        ).order_by(
            Notification.created_at.desc()
        ).all()