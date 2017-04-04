import requests
from bs4 import BeautifulSoup

QUERY_URL = 'https://www.wikidata.org/w/api.php'
# https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Bujumbura&language=en

def filterUnwanted(item):
    href = item.get('href')
    if 'List' in href or 'edit' in href:
        return False
    return True

# get the request
raw_wiki = requests.get('https://en.wikipedia.org/wiki/Wikipedia:WikiAfrica/African_cities')
# parse the request
wiki_soup = BeautifulSoup(raw_wiki.text, 'html.parser')

a_tags = filter(filterUnwanted, wiki_soup.select('#mw-content-text h2 + div a'))

for a_item in a_tags:
    r = requests.get(QUERY_URL, {'action': 'wbsearchentities', 'search': a_item.get_text(), 'language': 'en', 'format': 'json'})
    print(r.json()['search'])
