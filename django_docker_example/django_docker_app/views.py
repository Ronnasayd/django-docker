from django.shortcuts import render,redirect
from django.views import View
from .models import *

# Create your views here.


class Home(View):
	def get(self,request):
		if request.method == 'GET':
			return render(request,'home.html')

class Save(View):
	def post(self,request):
		if request.method == 'POST':
			dduser = DDUser.objects.create(email=request.POST['email'])
			dduser.save()
			return redirect('/')
		
