from django.shortcuts import render, redirect, HttpResponse
import uuid
from django.http import HttpResponseRedirect
import jwt

service_mapping = {"service1.local":"http://127.0.0.1:80","service2.local":"http://localhost:9001"}

HttpResponseRedirect.allowed_schemes.append('beyondc')

key = 'secret'
threshold = 0.5 


def agent_invoke(request,username):

	header_dict = dict(request.headers.items())
	#if request.META.get('HTTP_HOST') == "service1.local" and "Authorization" not in header_dict.keys():
	if "Authorization" not in header_dict.keys():
		link = "beyondc://service1?uuid=" + uuid.uuid4().__str__() + "&username=" + username
		print(link)
		return HttpResponseRedirect(link)

	else:
		service = request.META.get("HTTP_HOST")
		token = header_dict.get("Authorization")
		try:
			token = jwt.decode(token,key, algorithm='HS256')
			confidence = float(token.get('confidence'))

			if confidence > threshold:
				return redirect(service_mapping.get(service))

		except Exception as e:
			return HttpResponse("You are not authorized!")




