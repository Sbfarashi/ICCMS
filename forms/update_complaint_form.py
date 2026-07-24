from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    Length
)


class UpdateComplaintForm(FlaskForm):

    status = SelectField(
        "Complaint Status",
        choices=[
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Resolved", "Resolved"),
            ("Closed", "Closed")
        ],
        validators=[DataRequired()]
    )

    resolution = TextAreaField(
        "Resolution Notes",
        validators=[
            Optional(),
            Length(max=2000)
        ]
    )

    submit = SubmitField(
        "Update Complaint"
    )