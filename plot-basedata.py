#!/usr/bin/python3

"""
IN DEVELOPMENT
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()
sns.set_style("whitegrid")
sns.set_context("talk")

df = pd.read_csv("data/rki-cases_1584782859.tsv", sep="\t")

f = plt.figure(figsize=(20,10))

ax = sns.lineplot(x="Meldedatum", y="AnzahlFall", hue="Bundesland", data=df)

plt.savefig("cases.png")