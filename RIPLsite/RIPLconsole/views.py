from django.shortcuts import render
from RIPLapp.models import Bus

def index(request):
    return render(request, "console.html", {"console": Bus.objects.all()})
