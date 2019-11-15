from django.shortcuts import render, redirect
import uuid
from django.http import HttpResponseRedirect
import jwt
from jwt.exceptions import InvalidSignatureError


HttpResponseRedirect.allowed_schemes.append('beyondc')

key = 'secret'
threshold = 0.5 


def agent_invoke(request):

	link = "beyondc://service1?uuid=" + uuid.uuid4().__str__()
	return HttpResponseRedirect(link)



def score_checker(request):
	if request.method == "POST":
		try:
			token = request.POST.get("jwt")
			token = jwt.decode(token, key, algorithm='HS256')

			if token['confidence'] > threshold:
				# allow 

			else:
				# revoke

		except InvalidSignatureError as e:
			# revoke
