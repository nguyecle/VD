#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# imports ###################################################################

import sys
import json

from urllib.request import urlopen, urlretrieve, Request


# data ######################################################################

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
URL = "http://reports.weforum.org/global-gender-gap-report-2020/wp-content/themes/wef-reports/wef-components/dist/static/data/ggi/%s-%s/data.json"

for year in range(2016, 2019):
	req = Request(
		URL % (year, year+1),
		data=None, 
		headers={'User-Agent': UA}
	)
	response = urlopen(req)
	assert response.status == 200, "server responded %s" % response.status

	# getting encoding
	content_type = response.getheader('content-type').lower()
	assert content_type == "application/json"

	# parsing response
	raw_response = response.read()
	data = json.loads(raw_response)
	json.dump(data, open("ggi-%i.json" % year, "w"), indent=True)

