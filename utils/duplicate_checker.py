from models.complaint import Complaint


def complaint_exists(title):
    """
    Check whether a complaint with the same title
    already exists in the database.
    """

    complaint = Complaint.query.filter(
        Complaint.title.ilike(title)
    ).first()

    return complaint