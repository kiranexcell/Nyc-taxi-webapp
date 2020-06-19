from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, DateTimeLocalField
from wtforms import SubmitField, StringField
from wtforms.fields import DecimalField, SelectField, IntegerField
from wtforms.validators import DataRequired, AnyOf, NumberRange

class MyForm(FlaskForm):
    list_1_6 = []
    for i in range(1,7):
        list_1_6 += [(str(i),str(i))]

    vendor_id = SelectField('Vendor ID', choices=[('1', '1'), ('2', '2')],  validators=[DataRequired()])
    pickup_datetime = DateTimeLocalField('Pickup date and time',  format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    passenger_count = SelectField('Passenger count',choices= list_1_6, validators=[DataRequired()])
    pickup_longitude = DecimalField('Pickup longitude', validators=[DataRequired(), NumberRange(-122,-61,'Invalid input. Make sure that Pickup longitude is in between -61 and -122.')])
    pickup_latitude =  DecimalField('Pickup latitude', validators=[DataRequired(), NumberRange(32,52,'Invalid input. Make sure that Pickup latitude is in between 32 and 52.')])
    dropoff_longitude = DecimalField('Dropoff longitude', validators=[DataRequired(), NumberRange(-122,-61,'Invalid input. Make sure that Dropoff longitude is in between -61 and -122.')])
    dropoff_latitude =  DecimalField('Dropoff latitude', validators=[DataRequired(), NumberRange(32,52,'Invalid input. Make sure that Dropoff latitude is in between 32 and 52.')])
    submit = SubmitField('Predict')