import json 
from pymongo import MongoClient
from deepdiff import DeepDiff 
from flask import Flask 
from flask_restful import Api, Resource, reqparse
import requests 
import jwt 
from jwt.exceptions import InvalidSignatureError


# DB Initializers 
client =  MongoClient('localhost',27017)
db = client.mock
collection = db.deviceInfo

# Flask initializers
app = Flask(__name__)
api = Api(app)
key = 'secret'
URL = "127.0.0.1"


# Get the static list 
static_list = json.load(open("static_list_linux.json"))
user_privs = json.load(open("user_privs.json"))

static_list_items = list(static_list.keys())


table_names = ["authorized_keys","block_devices","chrome_extensions","deb_packages","disk_encryption","etc_services","firefox_addons","interface_addresses","interface_details","kernel_info","kernel_modules","listening_ports","mounts","os_version","platform_info","processes","rpm_packages","shadow","system_info","usb_devices","users","temp_uuid"]


class TrustScoreChecker(Resource):

	def post(self):
		parser = reqparse.RequestParser()
		for table in table_names:
			parser.add_argument(table,action='append')

		payload = parser.parse_args()
		uuid = payload.get("temp_uuid")[0]
		print(uuid)

		result = collection.find_one({"uuid":uuid})
		threshold = user_privs.get(uuid).get("score")
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
			post_id = collection.insert_one(payload).inserted_id 


		agent_details = {"uuid": uuid}
		if trust_score > threshold:
			agent_details["revoked"] = 0

		else:
			agent_details["revoked"] = 1
			

		token = jwt.encode(agent_details,key,algorithm='HS256').decode()
		#r = requests.post(URL, data = {"jwt" : token }) 
		print(token)
		print(agent_details)
		print(threshold)
		return token
		#return r.status_code 
		

api.add_resource(TrustScoreChecker,"/submit/")
app.run(host='0.0.0.0',port=9001, debug=True)







