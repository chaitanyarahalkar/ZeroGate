from django.shortcuts import render,redirect
from django.http import HttpResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
import uuid
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm
from django.contrib import messages
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

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return HttpResponse("Logged In")
    else:
        form = UserRegisterForm()
    return render(request, 'service/index.html', {'form': form})

def check_jwt(request):
	header_dict = dict(request.headers.items())
	if not "Authorization" in header_dict.keys():
		return redirect("http://127.0.0.1:8000/")
	else:
		return HttpResponse("You have token")



