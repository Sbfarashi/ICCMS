from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    Optional
)

from constants.roles import UserRole


class UserForm(FlaskForm):

    # ==========================================
    # Personal Information
    # ==========================================

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    employee_id = StringField(
        "Employee ID",
        validators=[
            Optional(),
            Length(max=20)
        ]
    )

    designation = StringField(
        "Designation",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    # ==========================================
    # Contact Information
    # ==========================================

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=11, max=20)
        ]
    )

    # ==========================================
    # Department
    # ==========================================

    department = SelectField(
        "Department",
        coerce=int,
        choices=[]
    )

    # ==========================================
    # Role
    # ==========================================

    role = SelectField(
        "Role",
        choices=[
            (UserRole.CUSTOMER, "Customer"),
            (UserRole.STAFF, "Staff"),
            (UserRole.ENGINEER, "Engineer"),
            (UserRole.SUPERVISOR, "Supervisor"),
            (UserRole.ADMIN, "Administrator")
        ]
    )

    # ==========================================
    # Password
    # ==========================================

    password = PasswordField(
        "Password",
        validators=[
            Optional(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            Optional(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    # ==========================================
    # Submit
    # ==========================================

    submit = SubmitField("Save User")