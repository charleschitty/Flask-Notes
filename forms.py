from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length

##User Forms

class RegisterForm(FlaskForm):
    """Form for registering an account"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)]
        )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=30)]
        )

    email = EmailField(
        "Email Address",
        validators=[InputRequired(), Length(max=50)]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)]
    )


class LoginForm(FlaskForm):
    """Form for logging into site"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )


#******************Note Forms**********************#

class AddNoteForm(FlaskForm):
    """Form to create a note"""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)]
        )

    content = TextAreaField(
        "Content",
        validators=[InputRequired()]
        )

class EditNoteForm(FlaskForm):
    """Form to change a note"""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)]
        )

    content = TextAreaField(
        "Content",
        validators=[InputRequired()]
        )


class CSRFValidationForm(FlaskForm):
    """Form to apply CSRF protection on logout"""