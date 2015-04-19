from django.shortcuts import render
from django_tables2 import RequestConfig
from RIPLapp.models import Bus, SOS, Volunteer
from RIPLconsole.tables import OperatorConsoleTable, SOSTable
from RIPLconsole.filters import SOSFilter, VolunteerFilter
from django.db.models import Count, Sum
from django.utils.safestring import mark_safe
import datetime

def index(request):
	vol_queryset = Volunteer.objects.select_related().all()
	vol_filter = VolunteerFilter(request.GET, queryset=vol_queryset)
	tracking = OperatorConsoleTable(vol_filter.qs)
	tracking.order_by = "volunteer_bus"
	RequestConfig(request, paginate={"per_page": 100}).configure(tracking)
	return render(request, 'console.html', {'tracking': tracking, 'vol_filter': vol_filter})


def sos(request):
	sos_queryset = SOS.objects.select_related().all()
	sos_filter = SOSFilter(request.GET, queryset=sos_queryset)
	sos_table = SOSTable(sos_filter.qs)
	RequestConfig(request).configure(sos_table)
	return render(request, 'sos.html', {'sos': sos_table, 'sos_filter': sos_filter})


def summary(request):
	# Expected numbers
	expected_num_buses = Bus.objects.count()
	expected_num_volunteers = Volunteer.objects.count()
	expected_num_children = Bus.objects.aggregate(child_sum=Sum('bus_expected_number_of_children')).get('child_sum')
	expected_num_adults = Bus.objects.aggregate(adult_sum=Sum('bus_expected_number_of_adults')).get('adult_sum')

	# Actual numbers
	actual_num_volunteers_reported_at_depot = Bus.objects.exclude(bus_volunteer_depot_login_time__isnull=True).count()
	actual_num_buses_started = Bus.objects.exclude(bus_started_from_depot_time__isnull=True).count()
        actual_num_children_pickedup = getSum(Bus.objects.aggregate(cm=Sum('bus_num_children_male_pickedup')).get('cm'),
                                             Bus.objects.aggregate(cf=Sum('bus_num_children_female_pickedup')).get('cf'))
        actual_num_adults_pickedup = getSum(Bus.objects.aggregate(am=Sum('bus_num_adults_male_pickedup')).get('am'),
                                             Bus.objects.aggregate(af=Sum('bus_num_adults_female_pickedup')).get('af'))
	actual_num_buses_debussed_at_stadium = Bus.objects.exclude(all_deboarded_at_stadium_time__isnull=True).count()
        actual_num_children_entered_stadium = getSum(Bus.objects.aggregate(cm=Sum('num_children_male_seated')).get('cm'),
                                             Bus.objects.aggregate(cf=Sum('num_children_female_seated')).get('cf'))
        actual_num_adults_entered_stadium = getSum(Bus.objects.aggregate(am=Sum('num_adults_male_seated')).get('am'),
                                             Bus.objects.aggregate(af=Sum('num_adults_female_seated')).get('af'))
	actual_num_buses_reached_drop_point = Bus.objects.exclude(everyone_dropped_off_time__isnull=True).count()
	actual_num_children_dropped = getSum(Bus.objects.aggregate(cm=Sum('bus_num_children_male_return_journey')).get('cm'),
	                             Bus.objects.aggregate(cf=Sum('bus_num_children_female_return_journey')).get('cf'))
        actual_num_adults_dropped = getSum(Bus.objects.aggregate(am=Sum('bus_num_adults_male_return_journey')).get('am'),
                                     Bus.objects.aggregate(af=Sum('bus_num_adults_female_return_journey')).get('af'))
	num_buses_with_volunteers = Volunteer.objects.exclude(volunteer_bus__isnull=True).distinct('volunteer_bus').count()

	# Deltas
	delta_volunteers_reported_at_depot = getDelta(actual_num_volunteers_reported_at_depot, expected_num_volunteers)
	delta_buses_started = getDelta(actual_num_buses_started, expected_num_buses)
	delta_children_pickedup = getDelta(actual_num_children_pickedup, expected_num_children)
        delta_adults_pickedup = getDelta(actual_num_adults_pickedup, expected_num_adults)
	delta_buses_debussed_at_stadium = getDelta(actual_num_buses_debussed_at_stadium, expected_num_buses)
        delta_children_entered_stadium = getDelta(actual_num_children_entered_stadium, expected_num_children)
        delta_adults_entered_stadium = getDelta(actual_num_adults_entered_stadium, expected_num_adults)
	delta_buses_reached_drop_point = getDelta(actual_num_buses_reached_drop_point, expected_num_buses)
	delta_children_dropped = getDelta(actual_num_children_dropped, expected_num_children)
        delta_adults_dropped = getDelta(actual_num_adults_dropped, expected_num_adults)
	delta_num_buses_with_volunteers = getDelta(num_buses_with_volunteers, expected_num_buses)

	return render(request,
	              'summary.html',
	              {'expected_num_buses': expected_num_buses,
		       'expected_num_volunteers': expected_num_volunteers,
		       'expected_num_children': expected_num_children,
		       'expected_num_adults': expected_num_adults,
		       'actual_num_volunteers_reported_at_depot': actual_num_volunteers_reported_at_depot,
	               'actual_num_buses_started': actual_num_buses_started,
		       'actual_num_children_pickedup': actual_num_children_pickedup,
		       'actual_num_adults_pickedup': actual_num_adults_pickedup,
	               'actual_num_buses_debussed_at_stadium': actual_num_buses_debussed_at_stadium,
		       'actual_num_children_entered_stadium': actual_num_children_entered_stadium,
		       'actual_num_adults_entered_stadium': actual_num_adults_entered_stadium,
	               'actual_num_buses_reached_drop_point': actual_num_buses_reached_drop_point,
		       'actual_num_children_dropped': actual_num_children_dropped,
		       'actual_num_adults_dropped': actual_num_adults_dropped,
	               'num_buses_with_volunteers': num_buses_with_volunteers,
		       'delta_volunteers_reported_at_depot': delta_volunteers_reported_at_depot,
	               'delta_buses_started': delta_buses_started,
		       'delta_children_pickedup': delta_children_pickedup,
		       'delta_adults_pickedup': delta_adults_pickedup,
	               'delta_buses_debussed_at_stadium': delta_buses_debussed_at_stadium,
		       'delta_children_entered_stadium': delta_children_entered_stadium,
		       'delta_adults_entered_stadium': delta_adults_entered_stadium,
	               'delta_buses_reached_drop_point': delta_buses_reached_drop_point,
		       'delta_children_dropped': delta_children_dropped,
		       'delta_adults_dropped': delta_adults_dropped,
	               'delta_num_buses_with_volunteers': delta_num_buses_with_volunteers, })

def getSum(addend1, addend2):
	if addend1 is None or addend2 is None:
		return 0
	return addend1 + addend2

def getDelta(actual, expected):
	delta = actual - expected

	if delta == 0:
		return delta
	else:
		return mark_safe('<span style="background-color: yellow">%s</span>' % delta)
