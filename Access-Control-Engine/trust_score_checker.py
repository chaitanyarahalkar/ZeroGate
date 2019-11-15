import jwt
from flask import Flask 
from flask_restful import Api, Resource, reqparse
from jwt.exceptions import InvalidSignatureError

key = 'secret'

app = Flask(__name__)
api = Api(app)

class Users(Resource):

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("confidence")
		agent_details = parser.parse_args()
		agent_details['confidence'] = float(agent_details['confidence'])

		if agent_details['confidence'] > 0.5:
			encoded = jwt.encode(agent_details,key,algorithm='HS256')
			return {'token': encoded.decode('ascii')},200
		else:
			return {'error':'Trust score is below threshold'},404

	def get(self,agent_details):
		pass


class Verifier(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument("token")
			token = parser.parse_args()
			decoded = jwt.decode(token['token'],'secret',algorithm='HS256')
			return  decoded,200

		except InvalidSignatureError as e:
			return {'error':'Invalid signature'},404



api.add_resource(Users,"/login/")
api.add_resource(Verifier,"/verify/")

app.run(host='0.0.0.0',port=8080,debug=True)

