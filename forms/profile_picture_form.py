from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField


class ProfilePictureForm(FlaskForm):

    profile_picture = FileField(
        "Profile Picture",
        validators=[
            FileRequired(message="Please select an image."),
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Only JPG, JPEG and PNG images are allowed."
            )
        ]
    )

    submit = SubmitField("Upload Picture")