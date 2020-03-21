from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Kasutaja', validators=[DataRequired()])
    password = PasswordField('Parool', validators=[DataRequired()])
    submit = SubmitField('Sisene')


class AddBookForm(FlaskForm):
    title = StringField('Pealkiri', validators=[DataRequired(), Length(max=100)])
    author = StringField('Autor', validators=[DataRequired(), Length(max=100)])
    location = IntegerField('Riiuli number', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Lisa')


class AddLenderForm(FlaskForm):
    name = StringField('Eesnimi', validators=[DataRequired(), Length(max=50)])
    surname = StringField('Perekonnanimi', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Lisa')
