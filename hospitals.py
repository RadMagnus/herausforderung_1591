# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 12:05:31 2020

@author: Magnus
"""


import json
import pandas as pd

hospitals = pd.read_json('data/hospitals/icu-beds-20200322T000513Z_clean.json', orient='columns')
data = json.loads('data/hospitals/icu-beds-20200322T000513Z.json')
