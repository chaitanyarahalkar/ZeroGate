from django.shortcuts import render, redirect
import uuid
from django.http import HttpResponseRedirect

HttpResponseRedirect.allowed_schemes.append('beyondc')

def agent_invoke(request):

	link = "beyondc://service1?uuid=" + uuid.uuid4().__str__()
	return HttpResponseRedirect(link)