from django.shortcuts import render
from django_tables2   import RequestConfig
from RIPLapp.models  import SOS, Volunteer
from RIPLconsole.tables  import OperatorConsoleTable, SOSTable

def index(request):
    sos = SOSTable(SOS.objects.all())
    tracking = OperatorConsoleTable(Volunteer.objects.all())
    RequestConfig(request).configure(tracking)
    return render(request, 'console.html', {'tracking': tracking, 'sos': sos})
