from pymongo import MongoClient
import pprint
from flask import Flask 
from flask_restful import Api, Resource, reqparse
from jwt.exceptions import InvalidSignatureError

key = 'secret'

app = Flask(__name__)
api = Api(app)


client =  MongoClient('localhost',27017)
db = client.mock
collection = db.deviceInfo
#post is the json os data


table_names = ["authorized_keys","block_devices","chrome_extensions","deb_packages","disk_encryption","etc_services","firefox_addons","interface_addresses","interface_details","kernel_info","kernel_modules","listening_ports","mounts","os_version","platform_info","processes","rpm_packages","shadow","system_info","usb_devices","users"]


class Data(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		for table in table_names:
			parser.add_argument(table,action='append')


		details = parser.parse_args()
		print(details)
		post_id = collection.insert_one({"username":details}).inserted_id
		print("Inserted record: ")
		pprint.pprint(collection.find_one({"_id":post_id}))
		return {"Result":1},200
		

api.add_resource(Data,"/submit/")
app.run(host='0.0.0.0',port=9001, debug=True)


