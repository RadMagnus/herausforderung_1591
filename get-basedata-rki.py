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

an entry can contain multiple reported cases which are separated into 
different rows where infected and deceased cases are further divided.
the date contains information about the time but only the day is used 
so this column is cutted to only contain YYYY-MM-DD.
"""
def get_rki_with_timestamp():
    url = "https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv"
    response = requests.get(url)
    response.encoding = "utf-8"
    if not response or not response.status_code == 200:
        print("could not fetch api")
        sys.exit(1)
    response = response.text.split("\n")

    # removes the columns for the number of infected, deceased cases and adds
    # a new header for the status
    header = response[0].split(",")
    del header[5]
    del header[5]
    header.append("status")
    header = ",".join(header)

    new_response = [header]
    
    for row in response[1:-1]:
        r_arr = row.split(",")

        # removes the columns for the number of infected, deceased cases and adds
        # a new header for the status
        num_cases = int(r_arr[5])
        num_dead = int(r_arr[6])
        r_arr[8] = r_arr[8][:10]

        del r_arr[5]
        del r_arr[5]

        for i in range(num_cases):
            new_response.append(",".join(r_arr+["infected"]))
        for i in range(num_dead):
            new_response.append(",".join(r_arr+["deceased"]))

    new_response = "\n".join(new_response)
    
    return pd.read_csv(StringIO(new_response), sep=",")

df = get_rki_with_timestamp()

ts = str(int(time.time()))
outfile = os.path.join(sys.argv[1], "rki-cases_"+ts+".tsv")
res = df.to_csv(outfile, sep="\t")