from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Kasutaja', validators=[DataRequired()])
    submit = SubmitField('Sisene')


class BookForm(FlaskForm):
    title = StringField('Pealkiri', validators=[DataRequired(), Length(max=100)])
    author = StringField('Autor', validators=[DataRequired(), Length(max=100)])
    location = IntegerField('Riiuli number', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Lisa')


class LenderForm(FlaskForm):
    name = StringField('Eesnimi', validators=[DataRequired(), Length(max=50)])
    surname = StringField('Perekonnanimi', validators=[DataRequired(), Length(max=50)])
    code = StringField('Isikukood', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Lisa')


class BookLendForm(FlaskForm):
    code = StringField('Isikukood', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Laenuta')


class ConfirmButton(FlaskForm):
    submit = SubmitField('Kinnita')
