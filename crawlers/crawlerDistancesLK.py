#!/usr/bin/python3
import requests
import json
import matplotlib.pyplot as plt
import csv
import geopy.distance


class CrawlerDistancesLK:
    """
    Crawler Class for Distances between landkreise
    """

    name = 'LK Distances Crawler'

    def __init__(self):
        pass

    def crawl(self):
        """
        Get data from web service and save it as CSV (semicolon separated) in data/raw
        :return: true if done w/o errors
        """

        no_erros = True
        raw_json_path = '../data/raw/distancematrix/lk_osm.json'
        optim_json_path = '../data/raw/distancematrix/lk_osm_optim.json'

        # print('Get data from Open Street Map...')
        # params = (('data', "[out:json];" \
        #                    "area[admin_level=2][name=Deutschland][boundary=administrative]->.boundaryarea;" \
        #                    "rel(area.boundaryarea)[admin_level=6];" \
        #                    "map_to_area -> .all_level_8_areas;" \
        #                    "(.all_level_8_areas;);" \
        #                    "rel(pivot);" \
        #                    "out geom;"),)
        #
        # response = requests.get('http://overpass-api.de/api/interpreter', params=params)
        # osm_dict = json.loads(response.content)
        #
        # print('Save OSM data to JSON file')
        # with open(raw_json_path, 'w') as f:
        #     json.dump(osm_dict, f)

        # # Load Open Street Map Results
        # print('Load OSM data from file...')
        # with open(raw_json_path, 'r') as file:
        #     osm_dict = json.load(file)
        #
        # # Load Landkreise list and generate dict
        # print('Load Landkreise list data from file...')
        # lk_dict = {}
        # with open('../data/landkreise.tsv', 'r') as tsvfile:
        #     lk_table = csv.reader(tsvfile, delimiter="\t")
        #     for lk in lk_table:
        #         lk_dict[lk[0]] = {'name': lk[1]}
        #
        # # Try to match lk_dict and osm results
        # print('Match OSM data and Landkreise list')
        # for lk in osm_dict['elements']:
        #     if 'tags' not in lk: #  or (('name' not in lk['tags']) and ('de:regionalschluessel' not in lk['tags'])
        #         print('ERROR ("tags" not in dict): {}'.format(lk['tags']))
        #         no_erros = False
        #     else:
        #         match_done = False
        #         if 'de:amtlicher_gemeindeschluessel' in lk['tags']:
        #             lks = lk['tags']['de:amtlicher_gemeindeschluessel']
        #             if self.match_lk_key(lks, lk_dict, lk):
        #                 match_done = True
        #
        #         if not match_done and 'de:regionalschluessel' in lk['tags']:
        #             lks = lk['tags']['de:regionalschluessel']
        #             if self.match_lk_key(lks, lk_dict, lk):
        #                 match_done = True
        #
        #         if not match_done and 'name' in lk['tags']:
        #             pass
        #
        #         if not match_done:
        #             print('ERROR NO KEY: {}'.format(lk['tags']))
        #         name = lk['tags']['name']
        #
        # # Check if all Landkreise covered
        # for lk_key, lk_val in lk_dict.items():
        #     if 'osm' not in lk_val:
        #         print('{}: {}'.format(lk_key, lk_val))
        #         if lk_val['name'] == 'Berlin, Stadt':
        #             lk = self.get_area_by_name(name='Berlin', admin_level=4)[0]
        #             lk_val['osm'] = lk
        #         elif lk_val['name'] == 'Hamburg, Stadt':
        #             lk = self.get_area_by_name(name='Hamburg', admin_level=4)[1]
        #             #Why not fist element? -> https://de.wikipedia.org/wiki/Hamburg-Neuwerk
        #             lk_val['osm'] = lk
        #         else:
        #             print('Error')
        #
        # # Provide shortcuts to important geo locations and delete 'osm' tag
        # for lk_key, lk_val in lk_dict.items():
        #     lk_val['lat_min'] = lk_val['osm']['bounds']['minlat']
        #     lk_val['lat_max'] = lk_val['osm']['bounds']['maxlat']
        #     lk_val['lon_min'] = lk_val['osm']['bounds']['minlon']
        #     lk_val['lon_max'] = lk_val['osm']['bounds']['maxlon']
        #     lk_val['lat_c'] = lk_val['lat_min'] + (lk_val['lat_max'] - lk_val['lat_min']) / 2
        #     lk_val['lon_c']=lk_val['lon_min'] + (lk_val['lon_max'] - lk_val['lon_min']) / 2
        #     del lk_val['osm']
        #
        # # Save optimized lk_dict to JSON file
        # print('Save optimized lk_dict to JSON file...')
        # with open(optim_json_path, 'w') as f:
        #     json.dump(lk_dict, f)

        # Load optimized lk_dict
        print('Load optimized lk_dict from file...')
        with open(optim_json_path, 'r') as file:
            lk_dict_optim = json.load(file)

        # # Visualize Bounding Boxes of Landkreise
        # plt.figure()
        # for lk_key, lk_val in lk_dict_optim.items():
        #     coord = [[lk_val['lon_min'], lk_val['lat_min']],
        #              [lk_val['lon_min'], lk_val['lat_max']],
        #              [lk_val['lon_max'], lk_val['lat_max']],
        #              [lk_val['lon_max'], lk_val['lat_min']],
        #              [lk_val['lon_min'], lk_val['lat_min']]]
        #     xs, ys = zip(*coord)  # create lists of x and y values
        #     plt.plot(xs, ys)
        #
        #     plt.text(lk_val['lon_c'], lk_val['lat_c'], lk_val['name'], horizontalalignment='center', verticalalignment='center')
        #
        #     print('{}'.format(lk_key))
        #     print('  - name: {}'.format(lk_val['name']))
        #     print('  - lat_min: {}'.format(lk_val['lat_min']))
        #     print('  - lat_max: {}'.format(lk_val['lat_max']))
        #     print('  - lon_min: {}'.format(lk_val['lon_min']))
        #     print('  - lon_max: {}'.format(lk_val['lon_max']))
        #     print('  - lat_center: {}'.format(lk_val['lat_c']))
        #     print('  - lon_center: {}'.format(lk_val['lat_c']))
        # plt.show()

        # Generate distance matrix
        print("Generate distance matrix...")
        distance_matrix = [['distance in km'] + [lks for lks in lk_dict_optim]]
        for lk1_key, lk1_val in lk_dict_optim.items():
            row = [lk1_key]
            coord1 = (lk1_val['lat_c'], lk1_val['lon_c'])
            for lk2_key, lk2_val in lk_dict_optim.items():
                coord2 = (lk2_val['lat_c'], lk2_val['lon_c'])

                if lk1_key == lk2_key:
                    dist = 0
                else:
                    dist = geopy.distance.vincenty(coord1, coord2).km
                    dist = int(round(dist, 0))

                print('{} <-> {}: {}'.format(lk1_val['name'], lk2_val['name'], dist))
                row.append(dist)
            distance_matrix.append(row)

        # Save distance matrix
        with open('../data/prepared/lk_distance_matrix.tsv', 'w', newline='') as tsvfile:
            csv_writer = csv.writer(tsvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerows(distance_matrix)
        return True

    def match_lk_key(self, key, lk_dict, lk):
        match_done = False
        # Is there a direct match?
        if key in lk_dict:
            lk_dict[key]['osm'] = lk
            match_done = True
            # print('DIRECT DONE ({}): {}'.format(key, lk['tags']))

        # If no direct match, modify Landskreisschluessel
        tmp_lks = key
        if not match_done:
            # remove zeros at beginning
            while len(tmp_lks) > 2 and tmp_lks[0] == '0':
                tmp_lks = tmp_lks[1:]
                if tmp_lks in lk_dict:
                    lk_dict[tmp_lks]['osm'] = lk
                    match_done = True
                    # print('MODIFY 1 DONE ({}): {}'.format(tmp_lks, lk['tags']))
                    break
        if not match_done:
            # remove zeros at end
            while len(tmp_lks) > 2 and tmp_lks[-1] == '0':
                tmp_lks = tmp_lks[:-1]
                if tmp_lks in lk_dict:
                    lk_dict[tmp_lks]['osm'] = lk
                    match_done = True
                    # print('MODIFY 2 DONE ({}): {}'.format(tmp_lks, lk['tags']))
                    break
        return match_done

    def get_area_by_name(self, name, admin_level):
        params = (('data', "[out:json];" \
                           "area[admin_level=" + str(admin_level) + "][name=" + name + "];" \
                           "nwr(pivot);" \
                           "out geom;"),)

        response = requests.get('http://overpass-api.de/api/interpreter', params=params)
        osm_dict = json.loads(response.content)
        return osm_dict['elements']



if __name__ == '__main__':
    c = CrawlerDistancesLK()
    c.crawl()
