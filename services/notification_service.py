from extensions import db
from models.notification import Notification


class NotificationService:

    # =====================================================
    # CREATE NOTIFICATION
    # =====================================================

    @staticmethod
    def create(
        user_id,
        title,
        message,
        notification_type="General"
    ):
        """
        Create a notification.

        NOTE:
        This method DOES NOT commit the transaction.
        The calling service (StaffService, AssignmentService,
        ComplaintService, etc.) should commit after all
        related operations have completed successfully.
        """

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )

        db.session.add(notification)

        return notification

    # =====================================================
    # GET USER NOTIFICATIONS
    # =====================================================

    @staticmethod
    def get_notifications(user_id):

        return (

            Notification.query

            .filter_by(
                user_id=user_id
            )

            .order_by(
                Notification.created_at.desc()
            )

            .all()

        )

    # =====================================================
    # GET SINGLE NOTIFICATION
    # =====================================================

    @staticmethod
    def get(notification_id):

        return Notification.query.get_or_404(
            notification_id
        )

    # =====================================================
    # UNREAD COUNT
    # =====================================================

    @staticmethod
    def unread_count(user_id):

        return (

            Notification.query

            .filter_by(
                user_id=user_id,
                is_read=False
            )

            .count()

        )

    # =====================================================
    # MARK AS READ
    # =====================================================

    @staticmethod
    def mark_as_read(notification_id):

        notification = Notification.query.get(
            notification_id
        )

        if notification is None:
            return False

        notification.is_read = True

        db.session.commit()

        return True

    # =====================================================
    # MARK ALL AS READ
    # =====================================================

    @staticmethod
    def mark_all_as_read(user_id):

        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).all()

        if not notifications:
            return 0

        for notification in notifications:
            notification.is_read = True

        db.session.commit()

        return len(notifications)

    # =====================================================
    # DELETE NOTIFICATION
    # =====================================================

    @staticmethod
    def delete(notification_id):

        notification = Notification.query.get(
            notification_id
        )

        if notification is None:
            return False

        db.session.delete(notification)

        db.session.commit()

        return True

    # =====================================================
    # DELETE ALL NOTIFICATIONS
    # =====================================================

    @staticmethod
    def delete_all(user_id):

        notifications = Notification.query.filter_by(
            user_id=user_id
        ).all()

        if not notifications:
            return 0

        count = len(notifications)

        for notification in notifications:
            db.session.delete(notification)

        db.session.commit()

        return count

    # =====================================================
    # LATEST NOTIFICATIONS
    # =====================================================

    @staticmethod
    def latest(user_id, limit=5):

        return (

            Notification.query

            .filter_by(
                user_id=user_id
            )

            .order_by(
                Notification.created_at.desc()
            )

            .limit(limit)

            .all()

        )