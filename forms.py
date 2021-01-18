from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class GameForm(FlaskForm):
    playerOne = StringField('playerOne', validators=[DataRequired(), Length(min=2, max=20)])
    playerTwo = StringField('playerTwo', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('submit')