#!/usr/bin/python3
import sys, os
import time
from io import StringIO
import requests
import pandas as pd
import urllib

class CrawlerDemography1:  # TODO: Specify the class name in relation to the source or content of this dataset
    """
    Getting information about demography. Currently only data from fraction of over age 65 per LK
    """

    name = 'Demography Crawler 1'  # TODO: Specify the name

    def __init__(self):
        pass

    def crawl(self):
        try:
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

            outfile = os.path.join("../data/raw/demography_over65.tsv")
            df.to_csv(outfile, sep="\t")

        except Error:
            return False
        return True


def convert_perc_values(perc_str):
    idx = len(perc_str) - 3
    return float(perc_str[0:idx] + "." + perc_str[idx:len(perc_str) - 1])


def fixBerlin(df):
    entry = df[df["IdLandkreis"] == "11000"]
    fix = [[]]
    for i in range(1, 13):
        df = df.append(pd.DataFrame([[str(i + 11000), entry.iloc[0]["Name"], entry.iloc[0]["Fract_Over_65"]]],
                                    columns=['IdLandkreis', 'Name', 'Fract_Over_65']), ignore_index=True)
    return df


if __name__ == '__main__':
    c = CrawlerDemography1()
    c.crawl()
