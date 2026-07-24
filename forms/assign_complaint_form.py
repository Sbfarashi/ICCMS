from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    SubmitField
)

from wtforms.validators import DataRequired


class AssignComplaintForm(FlaskForm):

    staff = SelectField(
        "Assign To",
        coerce=int,
        choices=[],
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Assign Complaint"
    )