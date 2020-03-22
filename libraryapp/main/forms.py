from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Kasutaja', validators=[DataRequired()])
    submit = SubmitField('Sisene')
