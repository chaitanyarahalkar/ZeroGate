from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import User, Resources 
import json 
from pymongo import MongoClient
from deepdiff import DeepDiff 
import jwt 
import requests
# from jwt.exceptions import InvalidSignatureError


# DB Initializers 
client =  MongoClient('localhost',27017)
db = client.mock
collection = db.deviceInfo

# JWT Secret 
key = 'secret'
URL = "127.0.0.1"


# Get the static list 
static_list = json.load(open("../static_list_linux.json"))
static_list_items = list(static_list.keys())


table_names = ["authorized_keys","block_devices","chrome_extensions","deb_packages","disk_encryption","etc_services","firefox_addons","interface_addresses","interface_details","kernel_info","kernel_modules","listening_ports","mounts","os_version","platform_info","processes","rpm_packages","shadow","system_info","usb_devices","users","temp_uuid","service","username"]

@csrf_exempt
def trust_score_checker(request):
	payload = dict()

	if request.method == "POST":
		# print(request.body)
		# for table in table_names:
		# 	payload[table] = request.POST.get(table)
		payload = json.loads(request.body)

		uuid = payload["temp_uuid"]
		username = payload["username"]
		result = collection.find_one({"temp_uuid": uuid})
		role = User.objects.get(username = payload["username"]).role
		threshold =  Resources.objects.get(role = role).score
		service = Resources.objects.get(role = role).service 

		trust_score = 0.0 

		if result is not None:
			trust_score = 0.5

			for item in static_list_items:
				if item in result:
					if result[item] == static_list[item]:
						trust_score  += 0.01

					else:
						trust_score -= 0.01

				else:
					trust_score = 0

			print(trust_score)


			diff = DeepDiff(result, payload, ignore_order = True)
			if not 'iterable_item_added' in diff:
				trust_score += 0.01


			else:
				total_diffs = len(diff['iterable_item_added'])
				trust_score -= (total_diffs * 0.01)

		else:
			post_id = collection.insert_one(payload).inserted_id


		agent_details = {"uuid" : uuid, "service": service}

		if trust_score > threshold:
			agent_details["revoked"] = 0

		else:
			agent_details["revoked"] = 1


		token = jwt.encode(agent_details, key, algorithm='HS256').decode()

		r = requests.post("http://localhost:8000/submit/{}/".format(username),headers={'Authorization':token},data={'ok':1})

		return HttpResponse(token)

	else:
		return HttpResponse("GET not allowed!")
