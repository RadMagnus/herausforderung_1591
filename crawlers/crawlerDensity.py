#!/usr/bin/python3

import os
from io import StringIO
import pandas as pd
import urllib

class CrawlerDensity:
    """
    Getting info about the Population Size, county size and therefore the population density of a county
    """

    name = 'Population Crawler'

    def __init__(self):
        pass

    def crawl(self):
        try:
            df=pd.read_excel("https://www.inkar.de/documents/Referenz%20Gemeinden-GVB-Kreise_NUTS.xlsx", sheet_name="KRS" )[['krs17','krs17name','fl17','bev17','land','Unnamed: 27']]
            df = df.drop(df.index[[0]])
            df.columns = ['id_county', 'county', 'size','population','id_state','state']
            df["id_county"]=df["id_county"].map(lambda i:int(i/1000))
            df["density"] = df["population"]/df["size"]

            outfile = os.path.join("../data/prepared/population_density.tsv")
            df.to_csv(outfile, sep="\t",index=False)

        except:
            return False
        return True



if __name__ == '__main__':
    c = CrawlerDensity()
    c.crawl()
