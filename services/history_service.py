from datetime import datetime

from extensions import db

from models.complaint_history import ComplaintHistory


class HistoryService:
    """
    Handles all complaint history logging.
    """

    @staticmethod
    def log(
        complaint_id,
        action,
        previous_status=None,
        new_status=None,
        remarks=None,
        performed_by=None
    ):
        """
        Save an action to the complaint history table.
        """

        history = ComplaintHistory(
            complaint_id=complaint_id,
            action=action,
            previous_status=previous_status,
            new_status=new_status,
            remarks=remarks,
            performed_by=performed_by,
            created_at=datetime.utcnow()
        )

        db.session.add(history)

        return history