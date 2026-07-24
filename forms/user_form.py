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
    EqualTo
)

from constants.roles import UserRole


class UserForm(FlaskForm):

    full_name = StringField(

        "Full Name",

        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]

    )

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

    role = SelectField(

        "Role",

        choices=[

            (UserRole.CUSTOMER, "Customer"),

            (UserRole.STAFF, "Staff"),

            (UserRole.ENGINEER, "Engineer"),

            (UserRole.ADMIN, "Administrator")

        ]

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
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]

    )

    submit = SubmitField(

        "Create User"

    )