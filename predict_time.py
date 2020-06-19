from datetime import datetime
from math import radians, cos, sin, asin, sqrt 
import numpy as np
import pandas as pd
import xgboost as xgb
import pickle

def distance(lat1, lat2, lon1, lon2):  
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    r = 6371
       
    return(c * r) 

def classify(x):
    if x < 13 :
        return 1
    elif x < 18:
        return 2
    elif x < 20:
        return 3
    elif x < 25:
        return 4

avg_speed_list_by_hour = [17.63787807, 18.41463378, 18.82925094, 19.9086661 , 22.13821595,
                        24.41170075, 20.39156421, 15.59633836, 12.81117055, 12.48206764,
                        12.61223671, 12.30394739, 12.11070006, 12.2657687 , 11.9812302 ,
                        11.83439655, 12.31502931, 12.23347371, 12.51924744, 13.47620384,
                        15.17610128, 15.73406908, 15.94919624, 16.8246619 ]

def predict_time(vendor_id,pickup_datetime,passenger_count,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude):
    col = ['vendor_id', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude',
       'dropoff_latitude', 'distance', 'hour_bin_2', 'hour_bin_3',
       'hour_bin_4', 'day_2', 'day_3', 'day_4', 'day_5', 'day_6', 'day_7',
       'day_8', 'day_9', 'day_10', 'day_11', 'day_12', 'day_13', 'day_14',
       'day_15', 'day_16', 'day_17', 'day_18', 'day_19', 'day_20', 'day_21',
       'day_22', 'day_23', 'day_24', 'day_25', 'day_26', 'day_27', 'day_28',
       'day_29', 'day_30', 'day_31', 'passenger_count_2', 'passenger_count_3',
       'passenger_count_4', 'passenger_count_5', 'passenger_count_6']
    
    arr = []

    # Vendor id
    vendor_id = int(vendor_id)
    if vendor_id == 2 :
        vendor_id = 0
    arr.append(vendor_id)


    # Latitude ,longitude ,distance
    dist = distance(pickup_latitude,dropoff_latitude,pickup_longitude,dropoff_longitude)
    arr = arr + [pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,dist]

    # Hour bin
    hour_bin = classify(avg_speed_list_by_hour[pickup_datetime.hour])
    for h in range(2,5):
        if h == hour_bin :
            arr.append(1)
        else:
            arr.append(0)

    # Day
    day = pickup_datetime.day
    for d in range(2,32):
        if d == day :
            arr.append(1)
        else:
            arr.append(0)
    
    # Passenger count
    passenger_count = int(passenger_count)
    for pc in range(2,7):
        if pc == passenger_count :
            arr.append(1)
        else:
            arr.append(0)
    
    # Scaling
    col1 = ['pickup_longitude', 'pickup_latitude','dropoff_longitude', 'dropoff_latitude', 'distance']
    arr1 = arr[2:7]
    loaded_mmc = pickle.load(open('./models/mmc_v1.pkl', 'rb'))
    arr1 = np.array(arr1).reshape(1,-1) 
    arr1 = loaded_mmc.transform(pd.DataFrame(arr1, columns = col1))
    arr[2:7] = list(arr1.reshape(-1,))

    # Predicting time
    loaded_model = pickle.load(open('./models/model_v2.pkl', 'rb'))
    arr = np.array(arr).reshape(1,-1)
    predicted_time = loaded_model.predict(pd.DataFrame(arr, columns = col))

    return(predicted_time)
