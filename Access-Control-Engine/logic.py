import json 
from pymongo import MongoClient
from deepdiff import DeepDiff 

# DB Initializers 
client =  MongoClient('localhost',27017)
db = client.mock
collection = db.deviceInfo


# Get the static list 
static_list = json.load(open("static_list_linux.json"))


# Check the recieved payload - TODO - Convert this to API handler 
payload = json.load(open("../Agent/linux-final-data.json"))
uuid = payload["uuid"]


result = collection.find_one({"uuid":uuid})

static_list_items = list(static_list.keys())


# Checking for static list fields in the payload 
trust_score = 0.0

if result is not None:
	trust_score = 0.5

	# Checking if static list items match with the payload items 
	for item in static_list_items:
		if item in result:
			if result[item] == static_list[item]:
				trust_score += 0.01

			else:
				trust_score -= 0.01

		else:
			trust_score = 0


	# Diff between received payload and the saved payload 
	diff = DeepDiff(result, payload, ignore_order = True)
	if not 'iterable_item_added' in diff:
		trust_score += 0.01	

	else:
		total_diffs = len(diff['iterable_item_added'])
		trust_score -= (total_diffs * 0.01)

else:
	# insert the payload in the database
	pass 

print(trust_score) 


