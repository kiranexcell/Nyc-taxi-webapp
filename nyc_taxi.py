from flask import Flask, render_template, url_for, flash, redirect
from forms import MyForm
import numpy as np
from predict_time import predict_time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iuabsrifb'

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form = MyForm()
    if form.validate_on_submit():
        predicted_time = predict_time(form.vendor_id.data,form.pickup_datetime.data,form.passenger_count.data,float(form.pickup_longitude.data),
                                      float(form.pickup_latitude.data),float(form.dropoff_longitude.data),float(form.dropoff_latitude.data))
        predicted_time_min = np.round(predicted_time[0]/60, decimals = 2)
        plus_minus = chr(177)
        flash(f'Likely trip time is {predicted_time_min} {plus_minus} 4.6 minutes', 'success')
    else :
        for field, errors in form.errors.items():
            for error in errors:
                #flash(f'Not a valid input', 'danger')
                flash(error, 'danger')
    return render_template("predict.html", title = 'predict', form = form)

if __name__ == '__main__':
    app.run(debug=False)