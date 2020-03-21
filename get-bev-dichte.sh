#/bin/bash

# download excel sheet from: https://www.inkar.de/
# convert excel sheet to tsv

# extract following columns: kreis_id, kreis, size, population, bundesland_id, bundesland
cut -f1,2,3,4,27,28 bev_dichte.tsv > bev_dichte_reduced.tsv
