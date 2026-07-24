from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length

from constants.roles import UserRole


class RegisterForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=11, max=15)
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            (UserRole.CUSTOMER, "Customer"),
            (UserRole.STAFF, "Staff"),
            (UserRole.ENGINEER, "Engineer"),
            (UserRole.SUPERVISOR, "Supervisor"),
            (UserRole.ADMIN, "Administrator")
        ],
        default=UserRole.CUSTOMER,
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")