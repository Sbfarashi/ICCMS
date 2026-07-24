from flask import Flask, render_template

from config import Config

# ==========================================
# Extensions
# ==========================================

from extensions import db, bcrypt, migrate

# ==========================================
# Models
# ==========================================

from models.user import User
from models.complaint import Complaint
from models.category import Category
from models.complaint_history import ComplaintHistory
from models.notification import Notification

# ==========================================
# Services
# ==========================================

from services.bootstrap_service import BootstrapService

# ==========================================
# Blueprints
# ==========================================

from routes.auth import auth
from routes.customer import customer
from routes.complaint import complaint
from routes.staff import staff
from routes.admin import admin
from routes.notification import notification


def create_app():

    app = Flask(__name__)

    # ==========================================
    # Configuration
    # ==========================================

    app.config.from_object(Config)

    # ==========================================
    # Initialize Extensions
    # ==========================================

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # ==========================================
    # Create Database Tables
    # ==========================================

    with app.app_context():

        db.create_all()

        BootstrapService.bootstrap()

    # ==========================================
    # Register Blueprints
    # ==========================================

    app.register_blueprint(auth)
    app.register_blueprint(customer)
    app.register_blueprint(complaint)
    app.register_blueprint(staff)
    app.register_blueprint(admin)
    app.register_blueprint(notification)

    # ==========================================
    # Public Pages
    # ==========================================

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/services")
    def services():
        return render_template("services.html")

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    # ==========================================
    # Global Notifications
    # ==========================================

    @app.context_processor
    def inject_notifications():

        from flask import session

        unread_notifications = 0

        if session.get("logged_in"):

            unread_notifications = Notification.query.filter_by(
                user_id=session["user_id"],
                is_read=False
            ).count()

        return dict(
            unread_notifications=unread_notifications
        )

    print("=" * 60)
    print("Smart Meters Company Ltd")
    print("Intelligent Customer Complaint Management System")
    print("Application initialized successfully.")
    print("=" * 60)

    return app