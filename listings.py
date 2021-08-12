import requests, tabulate, json, csv, sys
from collections import defaultdict, OrderedDict

CONTRACT = "0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42"
traitMap = json.load(open('traitmap.json'))

affinities = defaultdict(set)
maxAffinities = defaultdict(set)
tokens = set()

counts = defaultdict(int)
wizMax = defaultdict(int)

affinityNum = 5

if len(sys.argv) > 1:
	affinityNum = int(sys.argv[1])

for trait in traitMap:
	for i in range(0, 2):
		for affinityGroup in traitMap[trait][i+2]:
			affinities[traitMap[trait][1]].add(affinityGroup)
			counts[affinityGroup] += 1

with open('wizards.csv') as csvfile:
	for row in csv.DictReader(csvfile):
		thisAffinity = defaultdict(set)
		for trait in ['body', 'familiar', 'head', 'prop', 'rune']:
			for group in affinities[row[trait]]:
				thisAffinity[group].add(row[trait])

		maxAffinity = len(list(filter(None, [row['body'], row['familiar'], row['head'], row['prop'], row['rune']])))

		for affinityMatch in sorted(thisAffinity.items(), key=lambda item: len(item[1]), reverse=True):
			thisMatch = len(affinityMatch[1])

			if thisMatch == maxAffinity and thisMatch == affinityNum:
				#print('%s,%s,%s,%s' % (row['token_id'],row['name'], thisMatch, affinityMatch[0]))

				tokens.add(row['token_id'])
				maxAffinities[affinityMatch[0]].add(row['name'])
				wizMax[row['token_id']] = affinityMatch[0]

tokens = list(tokens)
#print(len(tokens))

#for affinity in sorted(maxAffinities.items(), key = lambda item: len(item[1]), reverse =True):
#	print(affinity)

offset = 0
pageSize = 50
querystring = {"token_ids": [], "asset_contract_address": CONTRACT, "order_direction": "desc", "offset": "0", "limit": str(pageSize)}

results = []

while offset < len(tokens):
	thisQuery = querystring.copy()
	thisQuery['token_ids'] = tokens[offset:offset + pageSize]

	response = requests.request("GET", "https://api.opensea.io/api/v1/assets", params=thisQuery)
	print(response)

	for token in response.json()['assets']:
		thisToken = OrderedDict()

		thisToken['price'] = None
		thisToken['link'] = token['permalink']
		thisToken['id'] = token['token_id']
		thisToken['affinityOccurrences'] = counts[wizMax[thisToken['id']]]
		thisToken['affinityGroup'] = wizMax[thisToken['id']]
		

		if token['sell_orders'] and token['sell_orders'][0]['payment_token_contract']['symbol'] == 'ETH':
			thisToken['price'] = float(token['sell_orders'][0]['current_price']) / 1000000000000000000.0

		if thisToken['price']:
			results.append(thisToken)

	offset += pageSize

	if len(tokens) - offset < pageSize:
		pageSize = len(tokens) - offset

print(tabulate.tabulate(sorted(results, key = lambda i:i['price']), headers="keys"))
