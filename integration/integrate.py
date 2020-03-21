#!/usr/bin/python3

import os
import pandas as pd

preparedDir = "../data/prepared"

def createFilelist():
    files = []
    for file in os.listdir(preparedDir):
        files.append(preparedDir+"/"+file)
    return files

def combineFiles(files):
    df = None

    for file in files:
        t = pd.read_table(file,sep="\t")
        if df is not None:
            df = df.join(t.set_index("IdLandkreis"), on="IdLandkreis", how='outer')
        else:
            df = t
    return df


def writeIntegratedData(data):
    outfile = os.path.join("integrated.tsv")
    data.to_csv(outfile, sep="\t",index=False)


if __name__ == '__main__':
    files = createFilelist()
    data = combineFiles(files)
    writeIntegratedData(data)