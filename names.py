from collections import defaultdict
import requests, tabulate, csv, sys

matches = []
nameLength = 1

if len(sys.argv) > 1:
	nameLength = int(sys.argv[1])

# Read element data from CSV
with open('wizards.csv') as csvfile:
	for row in csv.DictReader(csvfile):
		if row['name'] and len(row['name'].split()) == nameLength:
			matches.append(row['token_id'])

querystring = {"token_ids":[],"asset_contract_address":"0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42","order_direction":"desc","offset":"0","limit":"50"}

count = 0
pageSize = 50
wizards = []

while count < len(matches):
	thisQuery = querystring.copy()
	thisQuery['token_ids'] = matches[count:count + pageSize]

	response = requests.request("GET", "https://api.opensea.io/api/v1/assets", params=thisQuery)

	for wizard in response.json()['assets']:
		thisWizard = {}

		thisWizard['name'] = wizard['name']
		thisWizard['id'] = wizard['token_id']
		thisWizard['link'] = wizard['permalink']
		thisWizard['price'] = None

		if wizard['sell_orders'] and wizard['sell_orders'][0]['sale_kind'] == 0:
			thisWizard['price'] = float(wizard['sell_orders'][0]['current_price']) / 1000000000000000000.0

		if thisWizard['price']:
			wizards.append(thisWizard)

	count += pageSize

	if len(matches) - count < pageSize:
		pageSize = len(matches) - count

print(tabulate.tabulate(sorted(wizards, key = lambda i:i['price']), headers="keys"))
