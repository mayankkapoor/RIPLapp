from django.shortcuts import render
from django_tables2 import RequestConfig
from RIPLapp.models import Bus, SOS, Volunteer
from RIPLconsole.tables import OperatorConsoleTable, SOSTable
from RIPLconsole.filters import SOSFilter, VolunteerFilter
from django.db.models import Count, Sum
from django.utils.safestring import mark_safe


def index(request):
	vol_queryset = Volunteer.objects.select_related().all()
	vol_filter = VolunteerFilter(request.GET, queryset=vol_queryset)
	tracking = OperatorConsoleTable(vol_filter.qs)
	RequestConfig(request).configure(tracking)
	return render(request, 'console.html', {'tracking': tracking, 'vol_filter': vol_filter})


def sos(request):
	sos_queryset = SOS.objects.select_related().all()
	sos_filter = SOSFilter(request.GET, queryset=sos_queryset)
	sos = SOSTable(sos_filter.qs)
	RequestConfig(request).configure(sos)
	return render(request, 'sos.html', {'sos': sos, 'sos_filter': sos_filter})


def summary(request):
	expected_num_buses = Bus.objects.count()
	actual_num_buses_started = Bus.objects.exclude(bus_started_from_depot_time__isnull=True).count()
	actual_num_buses_debussed_at_stadium = Bus.objects.exclude(all_deboarded_at_stadium_time__isnull=True).count()
	actual_num_buses_reached_drop_point = Bus.objects.exclude(everyone_dropped_off_time__isnull=True).count()
	try:
		expected_num_people = (Bus.objects.aggregate(child_sum=Sum('bus_expected_number_of_children')).get('child_sum') +
	                       Bus.objects.aggregate(adult_sum=Sum('bus_expected_number_of_adults')).get('adult_sum'))
	except TypeError, e:
		expected_num_people = 0
	try:
		actual_num_people_entered_stadium = (Bus.objects.aggregate(cm=Sum('num_children_male_seated')).get('cm') +
	                                     Bus.objects.aggregate(cf=Sum('num_children_female_seated')).get('cf') +
	                                     Bus.objects.aggregate(am=Sum('num_adults_male_seated')).get('am') +
	                                     Bus.objects.aggregate(af=Sum('num_adults_female_seated')).get('af'))
	except TypeError, e:
		actual_num_people_entered_stadium = 0
	try:
		actual_num_people_dropped = (Bus.objects.aggregate(cm=Sum('bus_num_children_male_return_journey')).get('cm') +
	                             Bus.objects.aggregate(cf=Sum('bus_num_children_female_return_journey')).get('cf') +
	                             Bus.objects.aggregate(am=Sum('bus_num_adults_male_return_journey')).get('am') +
	                             Bus.objects.aggregate(af=Sum('bus_num_adults_female_return_journey')).get('af'))
	except TypeError, e:
		actual_num_people_dropped = 0
	try:
		num_buses_with_volunteers = Volunteer.objects.exclude(volunteer_bus__isnull=True).distinct('volunteer_bus').count()
	except NotImplementedError, e:
		num_buses_with_volunteers = 0

	delta_buses_started = getDelta(actual_num_buses_started, expected_num_buses)
	delta_buses_debussed_at_stadium = getDelta(actual_num_buses_debussed_at_stadium, expected_num_buses)
	delta_buses_reached_drop_point = getDelta(actual_num_buses_reached_drop_point, expected_num_buses)
	delta_people_entered_stadium = getDelta(actual_num_people_entered_stadium, expected_num_people)
	delta_people_dropped = getDelta(actual_num_people_dropped, expected_num_people)
	delta_num_buses_with_volunteers = getDelta(num_buses_with_volunteers, expected_num_buses)

	return render(request,
	              'summary.html',
	              {'expected_num_buses': expected_num_buses,
	               'actual_num_buses_started': actual_num_buses_started,
	               'actual_num_buses_debussed_at_stadium': actual_num_buses_debussed_at_stadium,
	               'actual_num_buses_reached_drop_point': actual_num_buses_reached_drop_point,
	               'expected_num_people': expected_num_people,
	               'actual_num_people_entered_stadium': actual_num_people_entered_stadium,
	               'actual_num_people_dropped': actual_num_people_dropped,
	               'num_buses_with_volunteers': num_buses_with_volunteers,
	               'delta_buses_started': delta_buses_started,
	               'delta_buses_debussed_at_stadium': delta_buses_debussed_at_stadium,
	               'delta_buses_reached_drop_point': delta_buses_reached_drop_point,
	               'delta_people_entered_stadium': delta_people_entered_stadium,
	               'delta_people_dropped': delta_people_dropped,
	               'delta_num_buses_with_volunteers': delta_num_buses_with_volunteers, })


def getDelta(actual, expected):
	delta = actual - expected

	if delta == 0:
		return delta
	else:
		return mark_safe('<span style="background-color: yellow">%s</span>' % delta);
