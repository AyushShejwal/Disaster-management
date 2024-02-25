#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 17:40:15 2024

@author: abc
"""
import requests
from requests.auth import HTTPBasicAuth
import folium
'''register_url = 'https://api.watttime.org/register'
params = {'username': 'Ayush',
         'password': 'Dalla@123',
         'email': 'ashejwal@asu.edu',
         'org': 'sin city'}
rsp = requests.post(register_url, json=params)
print(rsp.text)

login_url = 'https://api.watttime.org/login'
rsp = requests.get(login_url, auth=HTTPBasicAuth('Ayush', 'Dalla@123'))
TOKEN = rsp.json()['token']
print(rsp.json())'''

'''params = {"latitude": "37.7749", "longitude": "-122.4194", "signal_type": "co2_moer"}
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
print(response.json())'''

#url = "https://api.watttime.org/v3/region-from-loc"

TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6ImJhc2ljIiwiaWF0IjoxNzA4ODM2MjAxLCJleHAiOjE3MDg4MzgwMDEsImlzcyI6IldhdHRUaW1lIiwic3ViIjoiQXl1c2gifQ.Bm1y-NcVGMQuuVStV90uoCiwhvsaXrn_8PCrncVIrl2ti43Bh7z0__14imykoOMJNhKjn9QepRz97FxlJuvaVOMOOTxXoGan0OkE9PKHlKyBO14FsUUO7-IVE5blhK9VLyJM7lGxra31h2MoUjE-dekhWuGe6AxM0tL5QiLZEi4vJEG529Omn8iXV3rJ714gOrtBl-4t-jQ9yIytuJyym75Z6GyVa1L9YUO7TuNcUtdSoKitBpxUDInlRcawtUGQprtrza71HVfAgA3RbszyZ-kKeFA1FVgeaJ0_BsVg39O0Xy96brXo51aAind_gqafn1FvcSDx5_SdL_mya1Gm0w"

url = "https://api.watttime.org/v3/forecast"


headers = {"Authorization": f"Bearer {TOKEN}"}
params = {
    "region": "CAISO_NORTH",
    "signal_type": "co2_moer",
}

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
forecast_data_json = response.json()

# Accessing the 'data' key to get the list of forecast points
forecast_data = forecast_data_json['data']



def check_forecast(forecast_data, threshold):
    """
    Checks the forecast data for any points below a certain threshold and for power failures.
    
    Parameters:
    - forecast_data: A list of dictionaries, each containing 'point_time' and 'value' keys.
    - threshold: The CO2 emissions threshold (in lbs CO2 per MWh).
    
    Returns:
    - A tuple containing two lists: points_below_threshold and power_failures.
      Both lists contain dictionaries from the original forecast data that meet their respective conditions.
    """
    points_below_threshold = []
    power_failures = []
    
    for point in forecast_data:
        if point['value'] < threshold:
            points_below_threshold.append(point)
        if point['value'] == 0:
            power_failures.append(point)
    
    return points_below_threshold, power_failures

threshold = 1000  # Example threshold value
points_below_threshold, power_failures = check_forecast(forecast_data, threshold)

print("Points below threshold:", points_below_threshold)
print("Power failures:", power_failures)