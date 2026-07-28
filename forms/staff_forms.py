from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    TextAreaField,
    StringField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional,
    EqualTo
)


class AssignEngineerForm(FlaskForm):
    engineer_id = SelectField(
        "Engineer",
        coerce=int,
        validators=[DataRequired()]
    )

    note = TextAreaField(
        "Assignment Note",
        validators=[Optional(), Length(max=500)]
    )

    submit = SubmitField("Assign Engineer")


class UpdateStatusForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[
            ("Pending", "Pending"),
            ("Assigned", "Assigned"),
            ("In Progress", "In Progress"),
            ("Resolved", "Resolved"),
            ("Closed", "Closed"),
        ],
        validators=[DataRequired()]
    )

    remarks = TextAreaField(
        "Remarks",
        validators=[
            DataRequired(),
            Length(min=5, max=1000)
        ]
    )

    submit = SubmitField("Update Status")


class StaffProfileForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=120)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    phone = StringField(
        "Phone",
        validators=[
            Optional(),
            Length(max=20)
        ]
    )

    current_password = PasswordField(
        "Current Password",
        validators=[Optional()]
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            Optional(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            EqualTo(
                "new_password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField("Save Changes")