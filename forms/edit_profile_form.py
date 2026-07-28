from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional
)


class EditProfileForm(FlaskForm):

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
            Email(),
            Length(max=120)
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=7, max=20)
        ]
    )

    designation = StringField(
        "Designation",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    submit = SubmitField(
        "Update Profile"
    )