from django.shortcuts import render,redirect
from django.views import View
from .models import *

# Create your views here.


class Home(View):
	"""
	Return the list of technologies utilized
	"""
	def get(self,request,*args, **kwargs):
		"""
			This method return a render instance with template and context
			Args:
				self: self instace of the classe Home
				request: the request instance
				*args:
				**kwargs:
			return:
				a render instance
		"""
		tecnologias=[
		{"name":"Docker",
		 "image":"images/tecnologias/docker.png",
		 "url":"https://www.docker.com/"},
		
		{"name":"Django",
		 "image":"images/tecnologias/django.png",
		 "url":"https://www.djangoproject.com/"},

		 {"name":"Gulp",
		 "image":"images/tecnologias/gulp.png",
		 "url":"https://gulpjs.com/"},

		  {"name":"Browsersync",
		 "image":"images/tecnologias/browsersync.png",
		 "url":"https://browsersync.io/"},

		 {"name":"Docker Compose",
		 "image":"images/tecnologias/docker-compose.png",
		 "url":"https://docs.docker.com/compose/"},

		 {"name":"Sass",
		 "image":"images/tecnologias/sass.svg",
		 "url":"https://sass-lang.com/"},

		 {"name":"Nodejs",
		 "image":"images/tecnologias/nodejs.png",
		 "url":"https://nodejs.org/en/"},

		 {"name":"Nginx",
		 "image":"images/tecnologias/nginx.png",
		 "url":"https://www.nginx.com/"},
		 {"name":"Dbeaver",
		 "image":"images/tecnologias/dbeaver.png",
		 "url":"https://dbeaver.io/"
		 },
		  {"name":"Portainer",
		 "image":"images/tecnologias/portainer.png",
		 "url":"https://www.portainer.io"
		 },
		]
		
		if request.method == 'GET':
			return render(request,'home.html',{"tecnologias":tecnologias})

class Save(View):
	"""
	Save a DDuser on the database
	"""
	def post(self,request):
		if request.method == 'POST':
			dduser = DDUser.objects.create(email=request.POST['email'])
			dduser.save()
			return redirect('/')
		
