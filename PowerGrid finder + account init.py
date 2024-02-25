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
print(rsp.text)'''

login_url = 'https://api.watttime.org/login'
rsp = requests.get(login_url, auth=HTTPBasicAuth('Ayush', 'Dalla@123'))
TOKEN = rsp.json()['token']

url = "https://api.watttime.org/v3/region-from-loc"

headers = {"Authorization": f"Bearer {TOKEN}"}
params = {"latitude": "37.7749", "longitude": "-122.4194", "signal_type": "co2_moer"}
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
print(response.json())


