from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeLocalField
from wtforms.validators import DataRequired, Length


class EventForm(FlaskForm):
    title = StringField('Title name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(max=50)])
    begin_at = DateTimeLocalField('Data ISO-format', validators=[DataRequired()])
    end_at = DateTimeLocalField('Data ISO-format', validators=[DataRequired()])
    max_users = StringField('Max user', validators=[DataRequired(), Length(min=1, max=3)])
    is_active = BooleanField('Active')
    submit = SubmitField('Create Event')

