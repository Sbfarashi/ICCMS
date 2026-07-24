import os

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    # ==================================================
    # APPLICATION SETTINGS
    # ==================================================

    SECRET_KEY = "smartmetercompany2026"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR,
        "database",
        "smartmeter.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==================================================
    # IMAGE UPLOAD SETTINGS
    # ==================================================

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif"
    }

    # ==================================================
    # DEFAULT ADMIN ACCOUNT
    # ==================================================

    DEFAULT_ADMIN_NAME = "System Administrator"

    DEFAULT_ADMIN_EMAIL = "admin@smartmeters.com"

    DEFAULT_ADMIN_PHONE = "08000000000"

    DEFAULT_ADMIN_PASSWORD = "Admin@12345"

    # ==================================================
    # COMPANY INFORMATION
    # ==================================================

    COMPANY_NAME = (
        "Smart Meters Company Ltd"
    )

    SYSTEM_NAME = (
        "Intelligent Customer Complaint Management System"
    )

    COMPANY_ADDRESS = (
        "Kaduna, Nigeria"
    )