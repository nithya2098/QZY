from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class QuizSubmitForm(FlaskForm):
    question = StringField('question', validators=[DataRequired()])
    AOption = StringField('AOption', validators=[DataRequired()])
    BOption = StringField('BOption', validators=[DataRequired()])
    COption = StringField('COption', validators=[DataRequired()])
    DOption = StringField('DOption', validators=[DataRequired()])
    Answer = StringField('Answer', validators=[DataRequired()])
    category = StringField('dropdownMenuButton', validators=[DataRequired()])
    submit = SubmitField('Add Question')
