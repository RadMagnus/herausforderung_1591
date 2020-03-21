#!/usr/bin/python3

"""
writes the sars covid cases to tsv file in given directory

__author__ = "Samuel Klein"
"""

import sys, os
import time
from io import StringIO
import requests
import pandas as pd

if len(sys.argv) < 2:
    print("no output directory given: script.py <path>")
    sys.exit()

"""
returns the basic numbers of reported cases
"""
def get_rki():
    url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=GEN,BEZ,EWZ,cases,deaths,BL,BL_ID,county,RS&returnGeometry=false&outSR=4326&f=json"
    response = requests.get(url)
    if not response or not response.status_code == 200:
        print("could not fetch api")
        sys.exit(1)
        return
    response = response.json()["features"]
    
    cases = [c["attributes"] for c in response]
    return pd.DataFrame(data=cases)

"""
returns the data with a datapoint for each reported case with 
timestamp (useful for timeseries)
"""
def get_rki_with_timestamp():
    url = "https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv"
    response = requests.get(url)
    response.encoding = "utf-8"
    if not response or not response.status_code == 200:
        print("could not fetch api")
        sys.exit(1)
    response = response.text
    
    return pd.read_csv(StringIO(response), sep=",")

df = get_rki_with_timestamp()

ts = str(int(time.time()))
outfile = os.path.join(sys.argv[1], "rki-cases_"+ts+".tsv")
res = df.to_csv(outfile, sep="\t")