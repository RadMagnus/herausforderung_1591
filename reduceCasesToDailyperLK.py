# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:24:40 2020

@author: Magnus
"""

import pandas as pd
import os

rki_cases = pd.read_csv('integration/integrated.tsv', sep='\t')

initDfColumns = ['date', 'id_county', 'county', 'id_state', 'state', 'size', 
           'population', 'density', 'demography_1', 'no_cases', 'cases_m',
           'cases_w', 'A00-A04', 'A05-A14', 'A15-A34', 'A35-A59', 'A60-A79', 
           'A80+',  'no_infected', 'no_deceased']

# reduce rki_cases to DataFrame, where 1 row = 1 LK per day
def reduceCases(rki_cases, initDfColumns):
    LK_day_df = pd.DataFrame(columns= initDfColumns)
    for tuplecase in rki_cases.groupby(['id_county', 'date']):
        df = tuplecase[1]
        LK_day_df = LK_day_df.append({'date': df['date'].iloc[0], 
                                'id_county': df['id_county'].iloc[0], 
                                'county': df['county'].iloc[0], 
                                'id_state': df['id_state'].iloc[0], 
                                'state': df['state'].iloc[0], 
                                'size': df['size'].iloc[0], 
                                'population' : df['population'].iloc[0], 
                                'density': df['density'].iloc[0], 
                                'demography_1': df['demography_1'].iloc[0], 
                                'no_cases': df.shape[0], 
                                'cases_m': len(df[df['sex'] == 'M']),
                                'cases_w':len(df[df['sex'] == 'W']), 
                                'A00-A04':len(df[df['agegroups'] == 'A00-A04']), 
                                'A05-A14':len(df[df['agegroups'] == 'A05-A14']), 
                                'A15-A34':len(df[df['agegroups'] == 'A15-A34']), 
                                'A35-A59':len(df[df['agegroups'] == 'A35-A59']), 
                                'A60-A79':len(df[df['agegroups'] == 'A60-A79']), 
                                'A80+':len(df[df['agegroups'] == 'A80+']), 
                                'no_infected':len(df[df['status'] == 'infected']), 
                                'no_deceased':len(df[df['status'] == 'deceased'])
                                }, ignore_index=True)
    return LK_day_df
  
def writeIntegratedData(data):
    outfile = os.path.join("data/reduced/reduceCasesToDailyLK.tsv")
    data.to_csv(outfile, sep="\t",index=False)

if __name__ == '__main__':
    data = reduceCases(rki_cases, initDfColumns)
    writeIntegratedData(data)