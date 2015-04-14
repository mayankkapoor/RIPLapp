from django.shortcuts import render
from django_tables2 import RequestConfig
from RIPLapp.models import SOS, Volunteer
from RIPLconsole.tables import OperatorConsoleTable, SOSTable
from RIPLconsole.filters import VolunteerFilter


def index(request):
	vol_queryset = Volunteer.objects.select_related().all()
	vol_filter = VolunteerFilter(request.GET, queryset=vol_queryset)
	sos = SOSTable(SOS.objects.all())
	tracking = OperatorConsoleTable(vol_filter.qs)
	RequestConfig(request).configure(tracking)
	return render(request, 'console.html', {'tracking': tracking, 'sos': sos, 'vol_filter': vol_filter})
