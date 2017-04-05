# What does it do?

This script does the following:
* On https://en.wikipedia.org/wiki/Wikipedia:WikiAfrica/African_cities it will get the name of all the cities
* It will query the wikiData API endpoint with the name of the city: ```https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Name&language=en&format=json```
* Using the label, entity ID and the concept URI it will query wikiData again to get all the data about the city as JSON
* It will compare the properties of the entity with the list of properties that are deemed useful
* It will write a csv file called sets.csv with 4 columns: Name, ID, amount of properties and list of properties

This script was written as part of the [Workshop WIKI SUPSI - Chapter 2](https://meta.wikimedia.org/wiki/Workshop_Wiki_SUPSI_-_Chapter_2) by Fabian Frei