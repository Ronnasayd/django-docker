from django.shortcuts import render
from django.views import View

# Create your views here.


class Home(View):
	def get(self,request):
		if request.method == 'GET':
			return render(request,'home.html')
