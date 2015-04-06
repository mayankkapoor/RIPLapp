from django.shortcuts import render
from django_tables2   import RequestConfig
from RIPLapp.models  import Bus, Volunteer
from RIPLconsole.tables  import OperatorConsoleTable

def index(request):
    table = OperatorConsoleTable(Volunteer.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'console.html', {'table': table})
