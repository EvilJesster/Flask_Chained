from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields.html5 import EmailField

# form for user signup
class SignUpForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=80)])
    email = EmailField('Email address', [DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=80)])
    password_repeat = PasswordField('Repeat Password',
                                    validators=[
                                        DataRequired(),
                                        Length(min=6, max=80),
                                        EqualTo('password')
                                    ])
    submit = SubmitField('Sign Up')

# form for user login
class LogInForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=80)])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=80)])
    submit = SubmitField('Log In')
