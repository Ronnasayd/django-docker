from django.shortcuts import render
from .forms import FormUsuario

# Create your views here.


def index(request):
	form = FormUsuario()
	return render(request,'index.html',{'form':form})

def manage(request):
	if request.method == "POST":
		form = FormUsuario(request.POST, request.FILES)
		if form.is_valid():
			usuario = form.save()
			return render(request,'dashboard.html',{'usuario':usuario})
		else:
			return render(request,'index.html',{'form':form})
