from datetime import datetime

from models.complaint import Complaint


def generate_reference_number():
    """
    Generate a unique complaint reference number.

    Example:
    SMC-2026-000001
    """

    year = datetime.now().year

    total = Complaint.query.count() + 1

    return f"SMC-{year}-{total:06d}"