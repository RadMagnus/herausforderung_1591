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
import urllib
import math

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


def convert_perc_values(perc_str):
    idx = len(perc_str) - 3
    return float(perc_str[0:idx] + "." + perc_str[idx:len(perc_str) - 1])


def get_over_65_perc():
    url = "https://www.demografie-portal.de/SharedDocs/Downloads/DE/ZahlenFakten/csv/Bevoelkerung_ueber65_ueber80.csv;jsessionid=73550DF8E76F85EB04E92B13E9100EF5.2_cid389?__blob=publicationFile&v=3"
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode("cp1252")
    file = text.split("\r\n")
    content = ""
    for i in range(19, len(file)):
        content += file[i] + "\n"
    df = pd.read_csv(StringIO(content), sep=";", dtype=str)
    df.columns = ['IdLandkreis', 'Name', 'Fract_Over_65']
    df["IdLandkreis"] = df["IdLandkreis"].map(lambda id: "0" + id if len(id) == 4 else id)
    df["Fract_Over_65"] = df['Fract_Over_65'].map(convert_perc_values)

    df = fixBerlin(df)

    # df = df.astype({'IdLandkreis':str,'Name':str,'Fract_Over_65':float})
    return df


def fixBerlin(df):
    entry = df[df["IdLandkreis"] == "11000"]
    fix = [[]]
    for i in range(1, 13):
        df = df.append(pd.DataFrame([[str(i + 11000), entry.iloc[0]["Name"], entry.iloc[0]["Fract_Over_65"]]],
                                    columns=['IdLandkreis', 'Name', 'Fract_Over_65']), ignore_index=True)
        # df=df.append(pd.DataFrame([[11000+i,entry['Name'],entry["Fract_Over_65"]]],
        # columns=['IdLandkreis', 'Name', 'Fract_Over_65']), ignore_index=True)
    return df


def add_age_data(df):
    toadd = get_over_65_perc()[['IdLandkreis', 'Fract_Over_65']]
    return df.join(toadd.set_index("IdLandkreis"), on="IdLandkreis", how='left')


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
            new_response.append(",".join(r_arr + ["infected"]))
        for i in range(num_dead):
            new_response.append(",".join(r_arr + ["deceased"]))

    new_response = "\n".join(new_response)
    df = pd.read_csv(StringIO(new_response), sep=",")
    df = df.astype(
        {"IdBundesland": int, "Bundesland": str, "Landkreis": str, "Altersgruppe": str, "Geschlecht": str,
         "ObjectId": int, "Meldedatum": str, "IdLandkreis": str, "status": str})
    return df


df = get_rki_with_timestamp()
df = add_age_data(df)

ts = str(int(time.time()))
outfile = os.path.join(sys.argv[1], "rki-cases_" + ts + ".tsv")
res = df.to_csv(outfile, sep="\t")
