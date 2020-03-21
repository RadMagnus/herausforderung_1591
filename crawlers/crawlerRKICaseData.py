#!/usr/bin/python3

import os
from io import StringIO
import requests
import pandas as pd

class CrawlerRKICaseData:  # TODO: Specify the class name in relation to the source or content of this dataset
    """
    Crawler for the Robert-Koch-Institut Case Reports
    """

    name = 'RKI Case Data Crawler'

    def __init__(self):
        pass

    def crawl(self):

        try:

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

            outfile = os.path.join("../data/prepared/rki-cases.tsv")
            df.to_csv(outfile, sep="\t")

        except Error:
            return False
        return True


if __name__ == '__main__':
    c = CrawlerRKICaseData()
    c.crawl()
