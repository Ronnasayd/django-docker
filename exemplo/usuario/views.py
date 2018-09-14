from django.shortcuts import render
from .forms import FormUsuario
from .models import Usuario

# Create your views here.


def index(request):
	form = FormUsuario()
	return render(request,'index.html',{'form':form})

def manage(request):
	if request.method == "POST":
		form = FormUsuario(request.POST, request.FILES)
		if form.is_valid():
			usuario = form.save()
			usuarios = Usuario.objects.all().exclude(nome=usuario.nome)
			return render(request,'dashboard.html',{'usuario':usuario,'usuarios':usuarios})
		else:
			return render(request,'index.html',{'form':form})
