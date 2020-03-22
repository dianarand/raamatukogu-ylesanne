from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class AddForm(FlaskForm):
    title = StringField('Pealkiri', validators=[DataRequired(), Length(max=100)])
    author = StringField('Autor', validators=[DataRequired(), Length(max=100)])
    location = IntegerField('Riiuli number', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Lisa')


class LendForm(FlaskForm):
    # time_limit = IntegerField('Laenutuse pikkus')
    code = StringField('Isikukood', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Laenuta')


class SearchForm(FlaskForm):
    title = StringField('Pealkiri', validators=[Length(max=100)])
    author = StringField('Autor', validators=[Length(max=100)])
    submit = SubmitField('Otsi')


class ConfirmButton(FlaskForm):
    submit = SubmitField('Kinnita')
