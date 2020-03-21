#!/usr/bin/python3

import os
import pandas as pd

crawledDir = "../data/crawled"
preparedDir = "../data/prepared"

def createFilelist(dir):
    files = []
    for file in os.listdir(dir):
        files.append(dir+"/"+file)
    return files

def combineFiles(files):
    df = None

    for file in files:
        print("Adding "+file)
        t = pd.read_table(file,sep="\t")
        if df is not None:
            df = df.join(t.set_index("id_county"), on="id_county", how='outer')
        else:
            df = t
    return df


def writeIntegratedData(data):
    outfile = os.path.join("integrated.tsv")
    data.to_csv(outfile, sep="\t",index=False)


def combinePreparedFiles(data,files):
    for file in files:
        print("Adding "+ file)
        if file.endswith("population_density.tsv"):
            t = pd.read_table(file, sep="\t")
            data = data.join(t[['id_county', 'size', 'population', 'density']].set_index("id_county"), on="id_county",
                             how="outer")
            continue
        if file.endswith("demography_over65.tsv"):
            t = pd.read_table(file, sep="\t")
            data = data.join(t[['id_county', 'demography_1']].set_index("id_county"), on="id_county", how="outer")

            continue
    return data


if __name__ == '__main__':
    data = combineFiles(createFilelist(crawledDir))
    data = combinePreparedFiles(data,createFilelist(preparedDir))

    writeIntegratedData(data)