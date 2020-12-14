from flask_wtf import FlaskForm
from datetime import date
from wtforms import StringField, TextAreaField, IntegerField, TextField, DateField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo, Length
                                )
from models import Entry



class EntryForm(FlaskForm):
    title = StringField(label="Title", validators=[
                                DataRequired(), 
                                Length(max=50)
                            ])
    content = TextAreaField("Project Description",
                            validators=[
                                DataRequired()
                            ])
    timestamp = DateField(label="Project Date:",
                    default=date.today(),
                        validators=[
                                DataRequired(),
                            ])

    time_spent = IntegerField(label="Time spent in minutes.",
                                validators=[
                                DataRequired(),
                            ])
    resources = TextField(validators=[
                            ])