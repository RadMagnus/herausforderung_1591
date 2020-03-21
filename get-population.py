#!/usr/bin/python3

import sys
import os
import pandas as pd

if len(sys.argv) < 2:
    print("no output directory given: script.py <path>")
    sys.exit()

df = pd.read_csv("data/bev_dichte_reduced.tsv", sep="\t")

# harmonizes landkreis ids to fit with the ids of other sources
def shorten(s):
    return int(s/1000)

df["kreis_id"] = df["kreis_id"].apply(shorten)

# calculates the population density
df["factor"] = round(df["population"] / df["size"], 0).astype(int)

bls = set()
# writes the landkreise with id to file
with open(os.path.join(sys.argv[1], "landkreise.tsv"), "w") as fw:
    for index, row in df.iterrows():
        fw.write(str(row["kreis_id"])+"\t"+row["kreis"]+"\n")

# writes the bundeslaender with id to file
with open(os.path.join(sys.argv[1], "bundeslaender.tsv"), "w") as fw:
    for index, row in df.iterrows():
        if not row["bundesland_id"] in bls:
            bls.add(row["bundesland_id"])
            fw.write(str(row["bundesland_id"])+"\t"+row["bundesland"]+"\n")

df.to_csv(os.path.join(sys.argv[1], "population_density.tsv"), sep="\t")