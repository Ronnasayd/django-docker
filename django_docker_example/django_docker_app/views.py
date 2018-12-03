from django.shortcuts import render,redirect
from django.views import View
from .models import *

# Create your views here.


class Home(View):
	def get(self,request):
		tecnologias=[
		{"name":"Docker",
		 "image":"dd_images/tecnologias/docker.png",
		 "url":"https://www.docker.com/"},
		
		{"name":"Django",
		 "image":"dd_images/tecnologias/django.png",
		 "url":"https://www.djangoproject.com/"},

		 {"name":"Gulp",
		 "image":"dd_images/tecnologias/gulp.png",
		 "url":"https://gulpjs.com/"},

		  {"name":"Browsersync",
		 "image":"dd_images/tecnologias/browsersync.png",
		 "url":"https://browsersync.io/"},

		 {"name":"Docker Compose",
		 "image":"dd_images/tecnologias/docker-compose.png",
		 "url":"https://docs.docker.com/compose/"},

		 {"name":"Sass",
		 "image":"dd_images/tecnologias/sass.svg",
		 "url":"https://sass-lang.com/"},

		 {"name":"Nodejs",
		 "image":"dd_images/tecnologias/nodejs.png",
		 "url":"https://nodejs.org/en/"},

		 {"name":"Nginx",
		 "image":"dd_images/tecnologias/nginx.png",
		 "url":"https://www.nginx.com/"},
		]
		
		if request.method == 'GET':
			return render(request,'home.html',{"tecnologias":tecnologias})

class Save(View):
	def post(self,request):
		if request.method == 'POST':
			dduser = DDUser.objects.create(email=request.POST['email'])
			dduser.save()
			return redirect('/')
		
