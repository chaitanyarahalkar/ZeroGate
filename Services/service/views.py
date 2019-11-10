from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import uuid
from django.http import HttpResponseRedirect
'''
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Welcome to BeyondCorp!'}
        #return Response(content)
        link = "beyondc://service1?uuid="+uuid.uuid4().__str__()
        return redirect(link)
        #return HttpResponseRedirect(link)
        #return Response(link)
'''
def home(request):
    return HttpResponse('Hello, World!')

def check_jwt(request):
	header_dict = dict(request.headers.items())
	if not "Authorization" in header_dict.keys():
		return redirect("http://127.0.0.1:8000/")
	else:
		return HttpResponse("You have token")

