from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sys
import json
from django.utils import timezone

from RIPLapp.models import Volunteer, Bus, SOS

# Create your views here.


def home_page(request):
	context = {}
	return render(request, 'home.html', context)


# function that returns JSON response for login screen
def request_obtain(request, param):
	if request.method == 'POST':
		param_data = request.POST.get(param, None)
	else:
		param_data = request.GET.get(param, None)
	return param_data


def get_bus_phone(request):
	bus_code_num = request_obtain(request, 'bus_code_num')
	volunteer_phone_num = request_obtain(request, 'volunteer_phone_num')
	if bus_code_num and volunteer_phone_num:
		# The success will be handled by respective API handlers
		return bus_code_num, volunteer_phone_num
	else:
		raise Exception(HttpResponse(
			"Either bus_code_num or volunteer_phone_num doesn't exist in your " + request.method + " request."))


@csrf_exempt
def screentest(request):
	if request.META.get('REMOTE_ADDR') != '127.0.0.1':
		return HttpResponse("FORBIDDEN")
	bus_code_num, volunteer_phone_num = get_bus_phone(request)
	response_data = response_data_dict(bus_code_num, volunteer_phone_num)
	return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def screen1login_response(request):
	bus_code_num, volunteer_phone_num = get_bus_phone(request)
	# With the above function, the below if check is redundant, still keeping it as it is
	# TODO clean up the if check after verifying it's not required
	if bus_code_num and volunteer_phone_num:
		# TODO: This allows association of a single phone w/ multiple buses, is it correct?
		# MK: No. multiple phones for 1 bus is possible. Multiple buses per phone should not be possible.
		response_data = response_data_dict(bus_code_num, volunteer_phone_num)
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		response = HttpResponse()
		response.status_code = 500
		return response("Either bus_code_num or volunteer_phone_num doesn't exist in your POST request.")


@csrf_exempt
def screen2bus_safe_response(request):
	time_now = timezone.now()
	screen2_vars = {'bus_safe_flag': 1,
	                'bus_safe_time': time_now,
	                'bus_furthest_screen': 2,
	                'bus_last_location_latitude': 0.0,
	                'bus_last_location_longitude': 0.0
	                }
	auto_vars = ['bus_safe_time']
	return screen_data_processing(request, screen2_vars, auto_vars)


@csrf_exempt
def screen3bus_supply_count(request):
	screen3_vars = {'bus_number_water_bottles_initial': 0,
	                'bus_number_food_packets_initial': 0,
	                'bus_number_tickets_initial': 0,
	                # There is some problem in toggling it back to false from True for the flags
	                # Changed boolean to int to hack around toggle problem  # 0 = False, Non-zero=True
	                'bus_first_aid_kit_available_flag': 0,  # 'everyone_dropped_off_flag': 0,
	                'bus_furthest_screen': 3,
	                'bus_last_location_latitude': 0.0,
	                'bus_last_location_longitude': 0.0
	                }
	return screen_data_processing(request, screen3_vars)


@csrf_exempt
def screen4bus_started_depot(request):
	time_now = timezone.now()
	screen4_vars = {'bus_started_from_depot_flag': 0,  # Default is 0 or False
	                'bus_started_from_depot_time': time_now,
	                'bus_furthest_screen': 4,
	                'bus_last_location_latitude': 0.0,
	                'bus_last_location_longitude': 0.0
	                }
	auto_vars = ['bus_started_from_depot_time']
	return screen_data_processing(request, screen4_vars, auto_vars)


def screen_data_processing(request, screen_vars, auto_vars=[]):
	bus_screen_status = 0
	auto_vars.append('bus_furthest_screen')
	bus_code_num, volunteer_phone_num = get_bus_phone(request)
	
	to_be_deleted = []
	for key in screen_vars:
		if key not in auto_vars:
			value = request_obtain(request, key)
			if not value:
				to_be_deleted.append(key)
			else:
				screen_vars[key] = value
	if len(to_be_deleted) > 0:
		for key in to_be_deleted:
			del screen_vars[key]

	for key in screen_vars:
		bus_screen_status += save_bus_param(bus_code_num, volunteer_phone_num, key, screen_vars[key])
	
	if bus_screen_status == 0:
		return HttpResponse("OK")  # There is no need to return complete bus data for screens 2-12.
	else:
		response = HttpResponse()
		response.status_code = 500
		return response


def save_bus_param(bus_code_num, volunteer_phone_num, param, param_value):
	query_buses = Bus.objects.filter(bus_code_num=bus_code_num, volunteer__volunteer_phone_num=volunteer_phone_num)
	if query_buses.count() == 0:
		# This call should always be on a pre existing bus
		# If a bus does not exist its an error
		return 1
	elif query_buses.count() == 1:
		bus = query_buses[0]
		setattr(bus, param, param_value)
		bus.save()
		if getattr(bus, param) == param_value:
			return 0
		else:
			return 1
	else:
		print "Error! More than 1 buses returned for given bus code and volunteer phone number. Should not be " \
		      "possible. Buses: ", query_buses
		return 1


# function to return the full data set we have for a bus and volunteer as a dict
def response_data_dict(bus_code_num, volunteer_phone_num):
	try:
		query_buses = Bus.objects.filter(bus_code_num=bus_code_num, volunteer__volunteer_phone_num=volunteer_phone_num)
		bus_data_dict = {}
		if query_buses.count() == 0:
			new_volunteer = Volunteer(volunteer_phone_num=volunteer_phone_num)
			new_bus = Bus(bus_code_num=bus_code_num)
			new_bus.save()
			new_volunteer.volunteer_bus = new_bus
			new_volunteer.save()
		elif query_buses.count() == 1:
			bus = query_buses[0]
			bus_data_dict = turn_bus_data_into_dict(bus, volunteer_phone_num)
		# print bus_data_dict
		else:
			print "Error! More than 1 buses returned for given bus code and volunteer phone number. Should not be " \
			      "possible. Buses: ", query_buses
		return bus_data_dict
	except Exception, e:
		print 'Oops, %s did not complete. Exception: %s' % (sys._getframe().f_code.co_name, e)


# Encapsulating mainly for DRY later.
def turn_bus_data_into_dict(bus, volunteer_phone_num):
	bus_data_dict = {}
	for attr, value in bus.__dict__.iteritems():
		if type(value) is not int:
			value = str(value)
		bus_data_dict[attr] = value
	bus_data_dict['volunteer_phone_num'] = volunteer_phone_num
	return bus_data_dict


# Screen 5 total people picked after last checkpoint
@csrf_exempt
def screen5_total_people_picked(request):
	time_now = timezone.now()
	screen5_vars = {'bus_num_children_male_pickedup': 0,
	                'bus_num_children_female_pickedup': time_now,
	                'bus_num_adults_male_pickedup': 0,
	                'bus_num_adults_female_pickedup': 0,
	                'bus_furthest_screen': 6,
	                'bus_last_location_latitude': 0.0,
	                'bus_last_location_longitude': 0.0
	                }
	auto_vars = ['all_deboarded_at_stadium_time']
	return screen_data_processing(request, screen5_vars, auto_vars)


@csrf_exempt
def screen6_everyone_deboarded(request):
	time_now = timezone.now()
	screen6_vars = {'all_deboarded_at_stadium_flag': 0,
	                'all_deboarded_at_stadium_time': time_now,
	                'bus_furthest_screen': 6,
	                'bus_last_location_latitude': 0.0,
	                'bus_last_location_longitude': 0.0
	                }
	auto_vars = ['all_deboarded_at_stadium_time']
	return screen_data_processing(request, screen6_vars, auto_vars)


@csrf_exempt
def screen7_seated_at_stadium_count(request):
	screen7_vars = {'num_children_male_seated': 0,
	                'num_children_female_seated': 0,
	                'num_adults_male_seated': 0,
	                'num_adults_female_seated': 0,
	                'bus_furthest_screen': 7,
	                'bus_last_location_latitude': 0.0,
	                'bus_last_location_longitude': 0.0
	                }
	return screen_data_processing(request, screen7_vars)


@csrf_exempt
def screen8_seated_for_return_journey(request):
	screen8_vars = {'bus_num_children_male_return_journey': 0,
	                'bus_num_children_female_return_journey': 0,
	                'bus_num_adults_male_return_journey': 0,
	                'bus_num_adults_female_return_journey': 0,
	                'bus_furthest_screen': 8,
	                'bus_last_location_latitude': 0.0,
	                'bus_last_location_longitude': 0.0
	                }
	return screen_data_processing(request, screen8_vars)


@csrf_exempt
def screen9_everyone_deboarded_final(request):
	time_now = timezone.now()
	screen9_vars = {'everyone_dropped_off_flag': 0,
	                'everyone_dropped_off_time': time_now,
	                'bus_furthest_screen': 9,
	                'bus_last_location_latitude': 0.0,
	                'bus_last_location_longitude': 0.0
	                }
	auto_vars = ['everyone_dropped_off_time']
	return screen_data_processing(request, screen9_vars, auto_vars)


@csrf_exempt
def screen10_submitted_ngo_form(request):
	time_now = timezone.now()
	screen10_vars = {'feedback_form_taken_from_ngo_flag': 0,
	                 'feedback_form_taken_from_ngo_time': time_now,
	                 'bus_furthest_screen': 10,
	                 'bus_last_location_latitude': 0.0,
	                 'bus_last_location_longitude': 0.0
	                 }
	auto_vars = ['feedback_form_taken_from_ngo_time']
	return screen_data_processing(request, screen10_vars, auto_vars)


@csrf_exempt
def sos_report(request):
	time_now = timezone.now()
	bus_code_num, volunteer_phone_num = get_bus_phone(request)
	query_buses = Bus.objects.filter(bus_code_num=bus_code_num, volunteer__volunteer_phone_num=volunteer_phone_num)
	if query_buses.count() == 1:
		sos_volunteer = Volunteer.objects.get(volunteer_phone_num=volunteer_phone_num, volunteer_bus=query_buses[0])
		new_sos = SOS.objects.create(sos_bus=query_buses[0], sos_volunteer=sos_volunteer, sos_raise_time=time_now)
	else:
		raise Exception("Error: Sos query_buses did not return a unique bus. Somethings off.")
	return HttpResponse("SOS with bus code {0:s} & volunteer phone number {1:s} saved at {2:s}.".format(new_sos.sos_bus,
	                                                                                                    new_sos.sos_volunteer,
	                                                                                                    str(
		                                                                                                    new_sos.sos_raise_time)))
