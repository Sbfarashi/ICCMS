from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    StringField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length
)


class ComplaintForm(FlaskForm):

    category = SelectField(
        "Complaint Category",
        coerce=int,
        choices=[],
        validators=[DataRequired()]
    )

    subject = StringField(
        "Complaint Subject",
        validators=[
            DataRequired(),
            Length(min=5, max=200)
        ]
    )

    description = TextAreaField(
        "Complaint Description",
        validators=[
            DataRequired(),
            Length(min=20)
        ]
    )

    submit = SubmitField(
        "Submit Complaint"
    )