#!/usr/bin/python3

"""
IN DEVELOPMENT
"""

import sys
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

sns.set()
sns.set_style("whitegrid")
sns.set_context("talk")

def generate_dates(date_min, date_max):
    start = datetime.datetime.strptime(date_min, "%Y-%m-%d")
    end = datetime.datetime.strptime(date_max, "%Y-%m-%d")
    step = datetime.timedelta(days=1)
    dates = []
    while start <= end:
        dates.append(start.date().strftime("%Y-%m-%d"))
        start += step
    return dates

df = pd.read_csv("data/rki-cases_1584787895.tsv", sep="\t")

date_min = df["Meldedatum"].min()
date_max = df["Meldedatum"].max()
bls = df["Bundesland"].unique()

tmp = dict()

s_bl = "Bundesland"
s_md = "Meldedatum"
s_s = "status"

for index, row in df.iterrows():
    if not row[s_bl] in tmp:
        tmp[row[s_bl]] = dict()
    if not row[s_md] in tmp[row[s_bl]]:
        tmp[row[s_bl]][row[s_md]] = {"infected": 0, "deceased": 0}

    tmp[row[s_bl]][row[s_md]][row[s_s]] = tmp[row[s_bl]][row[s_md]][row[s_s]] + 1

dates = generate_dates(date_min, date_max)

final = ["Bundesland,Datum,Anzahl_Krank,Anzahl_Tot"]

for bl in bls:
    current_infected = 0
    current_deceased = 0
    for d in dates:
        if bl in tmp and d in tmp[bl]:
            current_infected += tmp[bl][d]["infected"]
            current_deceased += tmp[bl][d]["deceased"]
        final.append(bl+","+d+","+str(current_infected)+","+str(current_deceased))

final = "\n".join(final)
df = pd.read_csv(StringIO(final), sep=",")

f = plt.figure(figsize=(20,10))

ax = sns.lineplot(x="Datum", y="Anzahl_Krank", hue="Bundesland", data=df[df["Datum"] > "2020-02-24"])

plt.xticks(rotation=90)
plt.savefig("plots/cases_infected.png", bbox_inches = "tight")

plt.clf()

ax = sns.lineplot(x="Datum", y="Anzahl_Tot", hue="Bundesland", data=df[df["Datum"] > "2020-02-24"])

plt.xticks(rotation=90)
plt.savefig("plots/cases_deceased.png", bbox_inches = "tight")