from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Kasutaja', validators=[DataRequired()])
    password = PasswordField('Parool', validators=[DataRequired()])
    submit = SubmitField('Sisene')


class AddBook(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(max=100)])
    author = StringField('author', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('submit')


class AddLender(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(max=50)])
    surname = StringField('author', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('submit')
