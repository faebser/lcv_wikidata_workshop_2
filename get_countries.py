import requests
from bs4 import BeautifulSoup

QUERY_URL = 'https://www.wikidata.org/w/api.php'
# https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Bujumbura&language=en


def filter_unwanted(item):
    href = item.get('href')
    if 'List' in href or 'edit' in href:
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
        return name, ''
    search = json['search'][0]
    print('found entity, label: {} and url {}'.format(search['label'], '{}.json'.format(search['concepturi'])))
    return search['label'], '{}.json'.format(search['concepturi'])


# get the request
raw_wiki = requests.get('https://en.wikipedia.org/wiki/Wikipedia:WikiAfrica/African_cities')
# parse the request
wiki_soup = BeautifulSoup(raw_wiki.text, 'html.parser')

a_tags = filter(filter_unwanted, wiki_soup.select('#mw-content-text h2 + div a'))

label_urls = map(name_to_wiki_entity_url, map(tag_to_name, a_tags))

print(list(label_urls))