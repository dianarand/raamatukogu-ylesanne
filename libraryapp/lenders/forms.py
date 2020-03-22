from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddForm(FlaskForm):
    name = StringField('Eesnimi', validators=[DataRequired(), Length(max=50)])
    surname = StringField('Perekonnanimi', validators=[DataRequired(), Length(max=50)])
    code = StringField('Isikukood', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Lisa')


class SearchForm(FlaskForm):
    surname = StringField('Perekonnanimi', validators=[Length(max=50)])
    code = StringField('Isikukood', validators=[Length(max=11)])
    submit = SubmitField('Otsi')
