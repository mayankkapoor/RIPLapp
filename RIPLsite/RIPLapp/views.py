from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.


def home_page(request):
	context = {}
	return render(request, 'home.html', context)


def screen1_response(request):
	return