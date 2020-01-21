from django.shortcuts import render, redirect, HttpResponse
import uuid
from django.http import HttpResponseRedirect
import jwt
from django.views.decorators.csrf import csrf_exempt
import requests

service_mapping = {"service1.local":"http://127.0.0.1:80","service2.local":"http://localhost:9001"}

HttpResponseRedirect.allowed_schemes.append('beyondc')

key = 'secret'
threshold = 0.5 

@csrf_exempt
def agent_invoke(request,username):

	header_dict = dict(request.headers.items())
	#if request.META.get('HTTP_HOST') == "service1.local" and "Authorization" not in header_dict.keys():
	if "Authorization" not in header_dict.keys():
		link = "beyondc://service1?uuid=" + uuid.uuid4().__str__() + "&username=" + username
		return HttpResponseRedirect(link)

	else:
		service = request.META.get("HTTP_HOST")
		token = header_dict.get("Authorization")
		try:
			token = jwt.decode(token,key, algorithm='HS256')
			revoked = bool(token.get('revoked'))
			if not revoked:
				return redirect(service_mapping.get(service))

			else:
				return redirect("http://service1.local/revoked")

		except Exception as e:
			print(e)
			return HttpResponse("You are not authorized!")




