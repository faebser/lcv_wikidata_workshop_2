"""
    Workshop Wiki SUPSI - Chapter 2
    Copyright (C) 2017  Fabian Frei

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import grequests
import requests
from bs4 import BeautifulSoup
import csv
from functools import partial
from itertools import zip_longest


QUERY_URL = 'https://www.wikidata.org/w/api.php'
properties = frozenset(['P18', 'P17', 'P1376', 'P206', 'P625', 'P6', 'P1082', 'P2046', 'P41', 'P421', 'P856'])


def filter_unwanted(item):
    href = item.get('href')
    if 'List' in href or 'edit' in href or 'Metropolitan' in href:
        return False
    return True


def tag_to_name(tag):
    name = tag.get_text()
    print('mapping tag to {}'.format(name))
    return name


def responses_to_json(item):
    json = item.json()['entities']
    key = list(json.keys())[0]
    return json[key]


def get_concept_url(item):
    if 'concepturi' in item:
        return '{}.json'.format(item['concepturi'])


def filter_items(item):
    if 'P31' in item['claims'] and item['claims']['P31'][0]['mainsnak']['datavalue']['value']['numeric-id'] == 515:
        return True
    return False


def name_to_wiki_entity_urls(name):
    print('searching for {}'.format(name))
    json = requests.get(QUERY_URL, {'action': 'wbsearchentities', 'search': name, 'language': 'en', 'format': 'json'}).json()
    if len(json['search']) is 0:
        print('no entity found in wikidata')
        return name, []
    return name, map(get_concept_url, json['search'])


def get_and_filter_wiki_urls(item):
    name, requests_to_do = item
    rs = (grequests.get(u) for u in list(requests_to_do))
    bla = grequests.map(rs)
    jsons = map(responses_to_json, bla)
    return name, filter(filter_items, jsons)


def json_to_claims_set(json):
    # print('calculating set size for  {}, {}'.format(name, entity_id))
    claims_set = properties.intersection(frozenset(json['claims'].keys()))
    print(claims_set)
    return len(claims_set)


def json_to_prop_count(json):
    claims_length = len(json['claims'].keys())
    print(claims_length)
    return claims_length


def map_json(item):
    name, entities = item
    entities = list(entities)
    return name, map(json_to_claims_set, entities), map(json_to_prop_count, entities)

# get the request
raw_wiki = requests.get('https://en.wikipedia.org/wiki/Wikipedia:WikiAfrica/African_cities')
# parse the request
wiki_soup = BeautifulSoup(raw_wiki.text, 'html.parser')

a_tags = filter(filter_unwanted, wiki_soup.select('#mw-content-text h2 + div a'))

name_urls_to_check = map(name_to_wiki_entity_urls, map(tag_to_name, a_tags))
ready_to_count = map(get_and_filter_wiki_urls, name_urls_to_check)
ready_to_insert = map(map_json, ready_to_count)

print('writing csv file')
with open('lengths.csv', 'w', newline='') as csv_file:
    sets_writer = csv.writer(csv_file)
    sets_writer.writerow(('Name', 'Total amount of props', 'Amount of props from list'))
    for name, claims_set, count in ready_to_insert:
        counts = zip_longest(count, claims_set, fillvalue=0)
        for row in counts:
            sets_writer.writerow((name, row[0], row[1]))
