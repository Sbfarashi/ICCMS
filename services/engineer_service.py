from datetime import datetime, date

import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from sqlalchemy import func, or_, case

from extensions import db

from forms.edit_profile_form import EditProfileForm
from models.user import User
from models.complaint import Complaint
from models.complaint_history import ComplaintHistory
from models.field_visit import FieldVisit

from constants.roles import UserRole


class EngineerService:

    # ==========================================================
    # ENGINEER DASHBOARD STATISTICS
    # ==========================================================

    @staticmethod
    def dashboard_statistics(user_id):

        today = date.today()

        return {

            "assigned": Complaint.query.filter_by(
                assigned_to=user_id
            ).count(),

            "pending": Complaint.query.filter_by(
                assigned_to=user_id,
                status="Pending"
            ).count(),

            "assigned_only": Complaint.query.filter_by(
                assigned_to=user_id,
                status="Assigned"
            ).count(),

            "in_progress": Complaint.query.filter_by(
                assigned_to=user_id,
                status="In Progress"
            ).count(),

            "resolved": Complaint.query.filter_by(
                assigned_to=user_id,
                status="Resolved"
            ).count(),

            "closed": Complaint.query.filter_by(
                assigned_to=user_id,
                status="Closed"
            ).count(),

            "today_jobs": Complaint.query.filter(
                Complaint.assigned_to == user_id,
                func.date(Complaint.created_at) == today
            ).count()
        }

    # ==========================================================
    # RECENT JOBS
    # ==========================================================

    @staticmethod
    def recent_jobs(user_id, limit=10):

        return (

            Complaint.query

            .filter(
                Complaint.assigned_to == user_id
            )

            .order_by(
                Complaint.created_at.desc()
            )

            .limit(limit)

            .all()

        )

    # ==========================================================
    # SEARCH MY JOBS
    # ==========================================================

    @staticmethod
    def search_jobs(

        user_id,

        search="",

        status="",

        priority="",

        sort="newest",

        page=1,

        per_page=10

    ):

        query = (

            Complaint.query

            .filter(
                Complaint.assigned_to == user_id
            )

            .join(

                User,

                Complaint.customer_id == User.id

            )

        )

        if search:

            keyword = f"%{search.strip()}%"

            query = query.filter(

                or_(

                    Complaint.complaint_number.ilike(keyword),

                    Complaint.title.ilike(keyword),

                    Complaint.meter_number.ilike(keyword),

                    User.full_name.ilike(keyword)

                )

            )

        if status:

            query = query.filter(

                Complaint.status == status

            )

        if priority:

            query = query.filter(

                Complaint.priority == priority

            )

        # ======================================================
        # SORTING
        # ======================================================

        if sort == "oldest":

            query = query.order_by(

                Complaint.created_at.asc()

            )

        elif sort == "priority":

            priority_order = case(

                (Complaint.priority == "Critical", 1),

                (Complaint.priority == "High", 2),

                (Complaint.priority == "Medium", 3),

                (Complaint.priority == "Low", 4),

                else_=5

            )

            query = query.order_by(priority_order)

        elif sort == "status":

            query = query.order_by(

                Complaint.status.asc()

            )

        elif sort == "complaint":

            query = query.order_by(

                Complaint.complaint_number.asc()

            )

        else:

            query = query.order_by(

                Complaint.created_at.desc()

            )

        return query.paginate(

            page=page,

            per_page=per_page,

            error_out=False

        )

    # ==========================================================
    # GET SINGLE JOB
    # ==========================================================

    @staticmethod
    def get_job(complaint_id):

        return Complaint.query.get_or_404(

            complaint_id

        )

    # ==========================================================
    # JOB HISTORY
    # ==========================================================

    @staticmethod
    def complaint_history(complaint_id):

        return (

            ComplaintHistory.query

            .filter_by(

                complaint_id=complaint_id

            )

            .order_by(

                ComplaintHistory.created_at.desc()

            )

            .all()

        )

    # ==========================================================
    # GET FIELD VISITS
    # ==========================================================

    @staticmethod
    def field_visits(complaint_id):

        return (

            FieldVisit.query

            .filter_by(

                complaint_id=complaint_id

            )

            .order_by(

                FieldVisit.created_at.desc()

            )

            .all()

        )
    # ==========================================================
    # CREATE FIELD VISIT
    # ==========================================================

    @staticmethod
    def create_field_visit(

        complaint_id,

        engineer_id,

        visit_date,

        arrival_time,

        departure_time,

        observations,

        root_cause,

        work_done,

        materials_used,

        meter_replaced=False,

        old_meter_number=None,

        new_meter_number=None,

        recommendation=None,

        before_photo=None,

        after_photo=None,

        customer_signature=None

    ):

        visit = FieldVisit(

            complaint_id=complaint_id,

            engineer_id=engineer_id,

            visit_date=visit_date,

            arrival_time=arrival_time,

            departure_time=departure_time,

            observations=observations,

            root_cause=root_cause,

            work_done=work_done,

            materials_used=materials_used,

            meter_replaced=meter_replaced,

            old_meter_number=old_meter_number,

            new_meter_number=new_meter_number,

            recommendation=recommendation,

            before_photo=before_photo,

            after_photo=after_photo,

            customer_signature=customer_signature

        )

        db.session.add(visit)

        db.session.commit()

        return visit

    # ==========================================================
    # UPDATE JOB STATUS
    # ==========================================================

    @staticmethod
    def update_status(

        complaint_id,

        status,

        performed_by,

        remarks=""

    ):

        complaint = Complaint.query.get_or_404(

            complaint_id

        )

        previous_status = complaint.status

        complaint.status = status

        if status == "Closed":

            complaint.closed_at = datetime.utcnow()

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint.id,

                action="Engineer Status Update",

                previous_status=previous_status,

                new_status=status,

                remarks=remarks,

                performed_by=performed_by

            )

        )

        db.session.commit()

        return complaint

    # ==========================================================
    # RECORD ENGINEER ACTIVITY
    # ==========================================================

    @staticmethod
    def record_activity(

        complaint_id,

        activity,

        performed_by

    ):

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint_id,

                action=activity,

                previous_status=None,

                new_status=None,

                remarks=activity,

                performed_by=performed_by

            )

        )

        db.session.commit()

    # ==========================================================
    # START WORK
    # ==========================================================

    @staticmethod
    def start_work(

        complaint_id,

        engineer_id

    ):

        complaint = Complaint.query.get_or_404(

            complaint_id

        )

        previous_status = complaint.status

        complaint.status = "In Progress"

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint.id,

                action="Work Started",

                previous_status=previous_status,

                new_status="In Progress",

                remarks="Engineer started field work.",

                performed_by=engineer_id

            )

        )

        db.session.commit()

        return complaint

    # ==========================================================
    # ARRIVED AT SITE
    # ==========================================================

    @staticmethod
    def arrived_at_site(

        complaint_id,

        engineer_id

    ):

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint_id,

                action="Arrived at Site",

                previous_status=None,

                new_status=None,

                remarks="Engineer arrived at customer location.",

                performed_by=engineer_id

            )

        )

        db.session.commit()

    # ==========================================================
    # INSPECTION STARTED
    # ==========================================================

    @staticmethod
    def inspection_started(

        complaint_id,

        engineer_id

    ):

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint_id,

                action="Inspection Started",

                previous_status=None,

                new_status=None,

                remarks="Inspection has commenced.",

                performed_by=engineer_id

            )

        )

        db.session.commit()

    # ==========================================================
    # METER TESTED
    # ==========================================================

    @staticmethod
    def meter_tested(

        complaint_id,

        engineer_id,

        remarks="Meter tested successfully."

    ):

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint_id,

                action="Meter Tested",

                previous_status=None,

                new_status=None,

                remarks=remarks,

                performed_by=engineer_id

            )

        )

        db.session.commit()
    # ==========================================================
    # WIRING CHECKED
    # ==========================================================

    @staticmethod
    def wiring_checked(

        complaint_id,

        engineer_id,

        remarks="Customer wiring inspected."

    ):

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint_id,

                action="Wiring Checked",

                previous_status=None,

                new_status=None,

                remarks=remarks,

                performed_by=engineer_id

            )

        )

        db.session.commit()

    # ==========================================================
    # METER REPLACED
    # ==========================================================

    @staticmethod
    def replace_meter(

        complaint_id,

        engineer_id,

        old_meter,

        new_meter

    ):

        complaint = Complaint.query.get_or_404(

            complaint_id

        )

        complaint.meter_number = new_meter

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint.id,

                action="Meter Replaced",

                previous_status=None,

                new_status=None,

                remarks=f"Meter changed from {old_meter} to {new_meter}.",

                performed_by=engineer_id

            )

        )

        db.session.commit()

        return complaint

    # ==========================================================
    # SUBMIT RESOLUTION REPORT
    # ==========================================================

    @staticmethod
    def submit_resolution(

        complaint_id,

        resolution,

        engineer_id

    ):

        complaint = Complaint.query.get_or_404(

            complaint_id

        )

        previous_status = complaint.status

        complaint.resolution = resolution

        complaint.status = "Resolved"

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint.id,

                action="Resolution Submitted",

                previous_status=previous_status,

                new_status="Resolved",

                remarks=resolution,

                performed_by=engineer_id

            )

        )

        db.session.commit()

        return complaint

    # ==========================================================
    # CLOSE JOB
    # ==========================================================

    @staticmethod
    def close_job(

        complaint_id,

        engineer_id

    ):

        complaint = Complaint.query.get_or_404(

            complaint_id

        )

        previous_status = complaint.status

        complaint.status = "Closed"

        complaint.closed_at = datetime.utcnow()

        db.session.add(

            ComplaintHistory(

                complaint_id=complaint.id,

                action="Job Closed",

                previous_status=previous_status,

                new_status="Closed",

                remarks="Complaint closed successfully.",

                performed_by=engineer_id

            )

        )

        db.session.commit()

        return complaint

    # ==========================================================
    # ENGINEER PERFORMANCE
    # ==========================================================

    @staticmethod
    def performance(user_id):

        total = Complaint.query.filter_by(

            assigned_to=user_id

        ).count()

        resolved = Complaint.query.filter_by(

            assigned_to=user_id,

            status="Resolved"

        ).count()

        closed = Complaint.query.filter_by(

            assigned_to=user_id,

            status="Closed"

        ).count()

        in_progress = Complaint.query.filter_by(

            assigned_to=user_id,

            status="In Progress"

        ).count()

        pending = Complaint.query.filter_by(

            assigned_to=user_id,

            status="Pending"

        ).count()

        assigned = Complaint.query.filter_by(

            assigned_to=user_id,

            status="Assigned"

        ).count()

        completed = resolved + closed

        completion_rate = 0

        if total > 0:

            completion_rate = round(

                (completed / total) * 100,

                2

            )

        return {

            "total": total,

            "assigned": assigned,

            "pending": pending,

            "in_progress": in_progress,

            "resolved": resolved,

            "closed": closed,

            "completed": completed,

            "completion_rate": completion_rate

        }

    # ==========================================================
    # TOTAL FIELD VISITS
    # ==========================================================

    @staticmethod
    def total_field_visits(

        engineer_id

    ):

        return FieldVisit.query.filter_by(

            engineer_id=engineer_id

        ).count()

    # ==========================================================
    # MY FIELD VISITS
    # ==========================================================

    @staticmethod
    def my_field_visits(

        engineer_id

    ):

        return (

            FieldVisit.query

            .filter_by(

                engineer_id=engineer_id

            )

            .order_by(

                FieldVisit.created_at.desc()

            )

            .all()

        )
    # ==========================================================
    # GET SINGLE FIELD VISIT
    # ==========================================================

    @staticmethod
    def get_field_visit(visit_id):

        return FieldVisit.query.get_or_404(
            visit_id
        )

    # ==========================================================
    # DELETE FIELD VISIT
    # ==========================================================

    @staticmethod
    def delete_field_visit(visit_id):

        visit = FieldVisit.query.get_or_404(
            visit_id
        )

        db.session.delete(visit)

        db.session.commit()

        return True

    # ==========================================================
    # UPDATE FIELD VISIT
    # ==========================================================

    @staticmethod
    def update_field_visit(

        visit_id,

        visit_date,

        arrival_time,

        departure_time,

        observations,

        root_cause,

        work_done,

        materials_used,

        recommendation,

        meter_replaced,

        old_meter_number,

        new_meter_number

    ):

        visit = FieldVisit.query.get_or_404(
            visit_id
        )

        visit.visit_date = visit_date
        visit.arrival_time = arrival_time
        visit.departure_time = departure_time
        visit.observations = observations
        visit.root_cause = root_cause
        visit.work_done = work_done
        visit.materials_used = materials_used
        visit.recommendation = recommendation
        visit.meter_replaced = meter_replaced
        visit.old_meter_number = old_meter_number
        visit.new_meter_number = new_meter_number

        db.session.commit()

        return visit

    # ==========================================================
    # MY OPEN JOBS
    # ==========================================================

    @staticmethod
    def open_jobs(engineer_id):

        return (

            Complaint.query

            .filter(

                Complaint.assigned_to == engineer_id,

                Complaint.status.in_([

                    "Assigned",

                    "Pending",

                    "In Progress"

                ])

            )

            .order_by(

                Complaint.created_at.desc()

            )

            .all()

        )

    # ==========================================================
    # MY COMPLETED JOBS
    # ==========================================================

    @staticmethod
    def completed_jobs(engineer_id):

        return (

            Complaint.query

            .filter(

                Complaint.assigned_to == engineer_id,

                Complaint.status.in_(

                    [

                        "Resolved",

                        "Closed"

                    ]

                )

            )

            .order_by(

                Complaint.closed_at.desc()

            )

            .all()

        )

    # ==========================================================
    # COUNT OPEN JOBS
    # ==========================================================

    @staticmethod
    def count_open_jobs(engineer_id):

        return Complaint.query.filter(

            Complaint.assigned_to == engineer_id,

            Complaint.status.in_(

                [

                    "Assigned",

                    "Pending",

                    "In Progress"

                ]

            )

        ).count()

    # ==========================================================
    # COUNT COMPLETED JOBS
    # ==========================================================

    @staticmethod
    def count_completed_jobs(engineer_id):

        return Complaint.query.filter(

            Complaint.assigned_to == engineer_id,

            Complaint.status.in_(

                [

                    "Resolved",

                    "Closed"

                ]

            )

        ).count()

    # ==========================================================
    # RECENT FIELD VISITS
    # ==========================================================

    @staticmethod
    def recent_field_visits(

        engineer_id,

        limit=10

    ):

        return (

            FieldVisit.query

            .filter_by(

                engineer_id=engineer_id

            )

            .order_by(

                FieldVisit.created_at.desc()

            )

            .limit(limit)

            .all()

        )

    # ==========================================================
    # TOTAL RESOLVED TODAY
    # ==========================================================

    @staticmethod
    def resolved_today(engineer_id):

        today = date.today()

        return Complaint.query.filter(

            Complaint.assigned_to == engineer_id,

            Complaint.status == "Resolved",

            func.date(

                Complaint.updated_at

            ) == today

        ).count()

    # ==========================================================
    # TOTAL CLOSED TODAY
    # ==========================================================

    @staticmethod
    def closed_today(engineer_id):

        today = date.today()

        return Complaint.query.filter(

            Complaint.assigned_to == engineer_id,

            Complaint.status == "Closed",

            func.date(

                Complaint.closed_at

            ) == today

        ).count()

    # ==========================================================
    # ENGINEER INFORMATION
    # ==========================================================

    @staticmethod
    def engineer_profile(user_id):

        return User.query.get_or_404(
            user_id
        )
    # ==========================================================
    # MONTHLY PERFORMANCE
    # ==========================================================

    @staticmethod
    def monthly_statistics(engineer_id):

        current_year = datetime.utcnow().year

        results = []

        for month in range(1, 13):

            total = Complaint.query.filter(

                Complaint.assigned_to == engineer_id,

                func.extract("year", Complaint.created_at) == current_year,

                func.extract("month", Complaint.created_at) == month

            ).count()

            resolved = Complaint.query.filter(

                Complaint.assigned_to == engineer_id,

                Complaint.status.in_(["Resolved", "Closed"]),

                func.extract("year", Complaint.created_at) == current_year,

                func.extract("month", Complaint.created_at) == month

            ).count()

            results.append({

                "month": month,

                "assigned": total,

                "resolved": resolved

            })

        return results

    # ==========================================================
    # AVERAGE RESOLUTION TIME
    # ==========================================================

    @staticmethod
    def average_resolution_time(engineer_id):

        complaints = Complaint.query.filter(

            Complaint.assigned_to == engineer_id,

            Complaint.closed_at.isnot(None)

        ).all()

        if not complaints:

            return 0

        total_hours = 0

        count = 0

        for complaint in complaints:

            if complaint.created_at and complaint.closed_at:

                hours = (

                    complaint.closed_at -

                    complaint.created_at

                ).total_seconds() / 3600

                total_hours += hours

                count += 1

        if count == 0:

            return 0

        return round(total_hours / count, 2)

    # ==========================================================
    # DASHBOARD SUMMARY
    # ==========================================================

    @staticmethod
    def dashboard_summary(engineer_id):

        performance = EngineerService.performance(engineer_id)

        return {

            "statistics": EngineerService.dashboard_statistics(engineer_id),

            "performance": performance,

            "recent_jobs": EngineerService.recent_jobs(engineer_id, 5),

            "recent_visits": EngineerService.recent_field_visits(engineer_id, 5),

            "average_resolution_time": EngineerService.average_resolution_time(engineer_id)

        }

    # ==========================================================
    # ACTIVITY SUMMARY
    # ==========================================================

    @staticmethod
    def activity_summary(engineer_id):

        history = ComplaintHistory.query.filter_by(

            performed_by=engineer_id

        ).order_by(

            ComplaintHistory.created_at.desc()

        ).limit(20).all()

        return history

    # ==========================================================
    # VERIFY ENGINEER
    # ==========================================================

    @staticmethod
    def is_engineer(user_id):

        user = User.query.get(user_id)

        if not user:

            return False

        return user.role == UserRole.ENGINEER

    # ==========================================================
    # GET ENGINEER
    # ==========================================================

    @staticmethod
    def get_engineer(user_id):

        return User.query.filter_by(

            id=user_id,

            role=UserRole.ENGINEER

        ).first()

    # ==========================================================
    # LIST ALL ENGINEERS
    # ==========================================================

    @staticmethod
    def all_engineers():

        return User.query.filter_by(

            role=UserRole.ENGINEER

        ).order_by(

            User.full_name.asc()

        ).all()

    # ==========================================================
    # ENGINEER WORKLOAD
    # ==========================================================

    @staticmethod
    def workload(engineer_id):

        assigned = Complaint.query.filter_by(

            assigned_to=engineer_id

        ).count()

        active = Complaint.query.filter(

            Complaint.assigned_to == engineer_id,

            Complaint.status.in_(

                [

                    "Assigned",

                    "Pending",

                    "In Progress"

                ]

            )

        ).count()

        completed = Complaint.query.filter(

            Complaint.assigned_to == engineer_id,

            Complaint.status.in_(

                [

                    "Resolved",

                    "Closed"

                ]

            )

        ).count()

        return {

            "assigned": assigned,

            "active": active,

            "completed": completed

        }
    # ==========================================================
    # UPDATE ENGINEER PROFILE
    # ==========================================================

    @staticmethod
    def update_profile(user_id, form):

        try:

            engineer = User.query.get_or_404(user_id)

            # ----------------------------------------------
            # Check duplicate email
            # ----------------------------------------------

            email_exists = User.query.filter(
                User.email == form.email.data.strip().lower(),
                User.id != user_id
            ).first()

            if email_exists:
                return False, "Email address already exists."

            # ----------------------------------------------
            # Check duplicate phone
            # ----------------------------------------------

            phone_exists = User.query.filter(
                User.phone == form.phone.data.strip(),
                User.id != user_id
            ).first()

            if phone_exists:
                return False, "Phone number already exists."

            # ----------------------------------------------
            # Update profile
            # ----------------------------------------------

            engineer.full_name = form.full_name.data.strip()

            engineer.email = form.email.data.strip().lower()

            engineer.phone = form.phone.data.strip()

            engineer.designation = (
                form.designation.data.strip()
                if form.designation.data
                else None
            )

            db.session.commit()

            return True, "Profile updated successfully."

        except Exception as e:

            db.session.rollback()

            return False, f"Failed to update profile: {str(e)}"

    # ==========================================================
    # UPLOAD PROFILE PICTURE
    # ==========================================================

    @staticmethod
    def upload_profile_picture(user_id, image_file):

        try:

            engineer = User.query.get_or_404(user_id)

            extension = image_file.filename.rsplit(".", 1)[1].lower()

            filename = f"{uuid.uuid4().hex}.{extension}"

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "profile_pictures"
            )

            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(
                upload_folder,
                secure_filename(filename)
            )

            image_file.save(filepath)

            if (
                engineer.profile_picture
                and engineer.profile_picture != "default_avatar.png"
            ):

                old_file = os.path.join(
                    upload_folder,
                    engineer.profile_picture
                )

                if os.path.exists(old_file):
                    os.remove(old_file)

            engineer.profile_picture = filename

            db.session.commit()

            return True, "Profile picture updated successfully."

        except Exception as e:

            db.session.rollback()

            return False, str(e)

    # ==========================================================
    # END OF ENGINEER SERVICE
    # ==========================================================