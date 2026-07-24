from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    DateField,
    SubmitField
)

from wtforms.validators import Optional


class SearchForm(FlaskForm):
    """
    Complaint Search & Filter Form
    """

    complaint_number = StringField(
        "Complaint Number",
        validators=[Optional()]
    )

    customer = StringField(
        "Customer Name",
        validators=[Optional()]
    )

    meter_number = StringField(
        "Meter Number",
        validators=[Optional()]
    )

    status = SelectField(
        "Status",
        choices=[
            ("", "All Status"),
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Resolved", "Resolved"),
            ("Closed", "Closed")
        ],
        validators=[Optional()]
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("", "All Priorities"),
            ("Critical", "Critical"),
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low")
        ],
        validators=[Optional()]
    )

    category = SelectField(
        "Category",
        choices=[
            ("", "All Categories")
        ],
        validators=[Optional()]
    )

    date_from = DateField(
        "Date From",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    date_to = DateField(
        "Date To",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    search = SubmitField(
        "Search"
    )

    reset = SubmitField(
        "Reset"
    )