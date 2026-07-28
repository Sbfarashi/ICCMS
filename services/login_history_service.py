from datetime import datetime

from flask import request

from extensions import db
from models.login_history import LoginHistory


class LoginHistoryService:

    # =====================================================
    # RECORD LOGIN
    # =====================================================

    @staticmethod
    def record_login(user):

        browser = request.user_agent.browser or "Unknown"

        operating_system = (
            request.user_agent.platform or "Unknown"
        )

        ip_address = request.remote_addr or "Unknown"

        history = LoginHistory(
            user_id=user.id,
            ip_address=ip_address,
            browser=browser,
            operating_system=operating_system,
            login_status="Success"
        )

        user.last_login = datetime.utcnow()

        db.session.add(history)
        db.session.commit()

        return history

    # =====================================================
    # RECORD LOGOUT
    # =====================================================

    @staticmethod
    def record_logout(user_id):

        history = (
            LoginHistory.query
            .filter_by(user_id=user_id)
            .order_by(LoginHistory.login_time.desc())
            .first()
        )

        if history and history.logout_time is None:

            history.logout_time = datetime.utcnow()

            db.session.commit()

    # =====================================================
    # USER LOGIN HISTORY
    # =====================================================

    @staticmethod
    def get_user_history(user_id):

        return (
            LoginHistory.query
            .filter_by(user_id=user_id)
            .order_by(LoginHistory.login_time.desc())
            .all()
        )

    # =====================================================
    # ALL LOGIN HISTORY
    # =====================================================

    @staticmethod
    def get_all_history():

        return (
            LoginHistory.query
            .order_by(LoginHistory.login_time.desc())
            .all()
        )