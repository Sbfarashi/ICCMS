from flask_wtf import FlaskForm

from wtforms import PasswordField
from wtforms import SubmitField

from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo
)


class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(

        "Current Password",

        validators=[
            DataRequired(),
            Length(min=6, max=100)
        ]
    )

    new_password = PasswordField(

        "New Password",

        validators=[
            DataRequired(),
            Length(min=6, max=100)
        ]
    )

    confirm_password = PasswordField(

        "Confirm New Password",

        validators=[
            DataRequired(),
            EqualTo(
                "new_password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField(
        "Change Password"
    )