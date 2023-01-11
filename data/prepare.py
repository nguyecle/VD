#! /usr/bin/env python3

# imports ###################################################################

import sys
import csv
from collections import defaultdict


# country codes #############################################################

country_codes = csv.reader(open('iso-3166.csv'))
headers = next(country_codes)
assert headers == ['Global Code', 'Global Name', 'Region Code', 'Region Name', 'Sub-region Code', 'Sub-region Name', 'Intermediate Region Code', 'Intermediate Region Name', 'Country or Area', 'M49 Code', 'ISO-alpha2 Code', 'ISO-alpha3 Code', 'Least Developed Countries (LDC)', 'Land Locked Developing Countries (LLDC)', 'Small Island Developing States (SIDS)', 'Developed / Developing Countries']

iso3 =      headers.index('ISO-alpha3 Code')
region =    headers.index('Region Name')
subregion = headers.index('Sub-region Name')
country =   headers.index('Country or Area')

codes = {}
for raw in country_codes:    
    codes[raw[iso3]] = (raw[country], raw[subregion], raw[region])


# data ######################################################################

rows = csv.reader(open('data.csv'))
headers = next(rows)
assert headers == ['Country ISO3', 'Country Name', 'Indicator Id', 'Indicator', 'Subindicator Type', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

indicators = {
    "Overall Global Gender Gap Index":                                   'glob',
    "Global Gender Gap Economic Participation and Opportunity Subindex": 'eco',
    "Global Gender Gap Educational Attainment Subindex":                 'edu',
    "Global Gender Gap Health and Survival Subindex":                    'health',
    "Global Gender Gap Political Empowerment subindex":                  'pol',
}
subtypes = {
    "Rank": 'r',
    "Index": 'i',
}

countries = set()
dataset = defaultdict(list)

for row in rows:
    country, _, _, indicator, subtype, *values = row
    if indicator not in indicators:
        continue
    countries.add(country)
    indicator = indicators[indicator]
    subtype = subtypes[subtype]
    
    dataset[country, indicator, subtype] = list(float(v if v else 'nan') for v in values)


# output ####################################################################

gggi = open('gggi.tsv', 'w')
iso3 = open('iso3.tsv', 'w')

print('#alpha3', 'indicator', 'year', 'index', 'rank', sep='\t', file=gggi)
print('#alpha3', 'country', 'subregion', 'region', sep='\t', file=iso3)
for country in sorted(countries):
    for indicator in ['glob', 'eco', 'edu', 'health', 'pol']:
        for y, i, r in zip(
            range(2006, 2021),
            dataset[country, indicator, 'i'],
            dataset[country, indicator, 'r'],
        ):
            print(country, indicator, y, i, r, sep='\t', file=gggi)
    print(country, *codes[country], sep='\t', file=iso3)
