import requests
from bs4 import BeautifulSoup
import csv

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


def name_to_wiki_entity_url(name):
    print('searching for {}'.format(name))
    json = requests.get(QUERY_URL, {'action': 'wbsearchentities', 'search': name, 'language': 'en', 'format': 'json'}).json()
    if len(json['search']) is 0:
        print('no entity found in wikidata')
        return name, '', None
    search = json['search'][0]
    print('found entity, label: {} and url {}'.format(search['label'], '{}.json'.format(search['concepturi'])))
    return search['label'], search['id'], '{}.json'.format(search['concepturi'])


def wiki_entity_url_to_claims_set(item):
    name, entity_id, url = item
    print('getting data for {}, {}'.format(name, entity_id))
    if url is None and entity_id == '':
        return name, entity_id, frozenset()
    json = requests.get(url).json()
    claims_set = properties.intersection(frozenset(json['entities'][entity_id]['claims'].keys()))
    print(claims_set)
    return name, entity_id, claims_set

# get the request
raw_wiki = requests.get('https://en.wikipedia.org/wiki/Wikipedia:WikiAfrica/African_cities')
# parse the request
wiki_soup = BeautifulSoup(raw_wiki.text, 'html.parser')

a_tags = filter(filter_unwanted, wiki_soup.select('#mw-content-text h2 + div a'))

label_urls = map(name_to_wiki_entity_url, map(tag_to_name, a_tags))
sets = map(wiki_entity_url_to_claims_set, label_urls)

print('writing csv file')
with open('sets.csv', 'w', newline='') as csv_file:
    sets_writer = csv.writer(csv_file)
    sets_writer.writerow(('Name', 'Entity ID', 'Amount of props', 'Props List'))
    for item in sets:
        sets_writer.writerow((item[0], item[1], len(item[2]), ','.join(item[2])))
