from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sys
import json
from django.utils import timezone

from RIPLapp.models import Volunteer, Bus

# Create your views here.


def home_page(request):
	context = {}
	return render(request, 'home.html', context)


# function that returns JSON response for login screen
def request_obtain(request, param):
	if request.method == 'POST':	
		param_data=request.POST.get(param, None)
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
		raise Exception(HttpResponse("Either bus_code_num or volunteer_phone_num doesn't exist in your "+request.method+" request."))

@csrf_exempt
def screen1login_response(request):
	bus_code_num,volunteer_phone_num = get_bus_phone(request)
	#With the above function, the below if check is redundant, still keeping it as it is
	#TODO clean up the if check after verifying it's not required
	if bus_code_num and volunteer_phone_num:
		# TODO: This allows association of a single phone w/ multiple buses, is it correct?
		# MK: No. multiple phones for 1 bus is possible. Multiple buses per phone should not be possible.
		response_data = response_data_dict(bus_code_num, volunteer_phone_num)
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		return HttpResponse("Either bus_code_num or volunteer_phone_num doesn't exist in your POST request.")

@csrf_exempt
def screen2bus_safe_response(request):
	bus_code_num, volunteer_phone_num = get_bus_phone(request)
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_safe_flag', True)
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_safe_time', timezone.now())  # UTC time
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_furthest_screen', 2)
	return HttpResponse("OK")  # There is no need to return complete bus data for screens 2-12.


def save_bus_param(bus_code_num, volunteer_phone_num, param, param_value):
	query_buses = Bus.objects.filter(bus_code_num=bus_code_num, volunteer__volunteer_phone_num=volunteer_phone_num)
	# print query_buses.count()
	if query_buses.count() == 0:
		new_volunteer = Volunteer(volunteer_phone_num=volunteer_phone_num)
		new_bus = Bus(bus_code_num=bus_code_num)
		new_bus.save()
		new_volunteer.volunteer_bus = new_bus
		new_volunteer.save()
		setattr(new_bus, param, param_value)
		new_bus.save()
		# print getattr(new_bus, param)
	elif query_buses.count() == 1:
		bus = query_buses[0]
		# print bus
		setattr(bus, param, param_value)
		bus.save()
		# print bus
		print getattr(bus, param) #TODO: Doesn't seem to work
	else:
		print "Error! More than 1 buses returned for given bus code and volunteer phone number. Should not be " \
		      "possible. Buses: ", query_buses

		
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
	bus_data_dict = {'bus_code_num': bus.bus_code_num, 'volunteer_phone_num': volunteer_phone_num,
	                 'bus_safe_flag': bus.bus_safe_flag, 'bus_safe_time': str(bus.bus_safe_time),
	                 'bus_expected_number_of_children': bus.bus_expected_number_of_children,
	                 'bus_expected_number_of_adults': bus.bus_expected_number_of_adults,
	                 'bus_number_food_packets_initial': bus.bus_number_food_packets_initial,
	                 'bus_number_water_bottles_initial': bus.bus_number_water_bottles_initial,
	                 'bus_started_from_depot_flag': bus.bus_started_from_depot_flag,
	                 'bus_started_from_depot_time': str(bus.bus_started_from_depot_time),
	                 'bus_first_aid_kit_available_flag': bus.bus_first_aid_kit_available_flag,
	                 'bus_num_children_male_pickedup': bus.bus_num_children_male_pickedup,
	                 'bus_num_children_female_pickedup': bus.bus_num_children_female_pickedup,
	                 'bus_num_adults_male_pickedup': bus.bus_num_adults_male_pickedup,
	                 'bus_num_adults_female_pickedup': bus.bus_num_adults_female_pickedup,
	                 'all_deboarded_at_stadium_flag': bus.all_deboarded_at_stadium_flag,
	                 'all_deboarded_at_stadium_time': str(bus.all_deboarded_at_stadium_time),
	                 'num_children_male_seated': bus.num_children_male_seated,
	                 'num_children_female_seated': bus.num_children_female_seated,
	                 'num_adults_male_seated': bus.num_adults_male_seated,
	                 'num_adults_female_seated': bus.num_adults_female_seated,
	                 'bus_num_children_male_return_journey': bus.bus_num_children_male_return_journey,
	                 'bus_num_children_female_return_journey': bus.bus_num_children_female_return_journey,
	                 'bus_num_adults_male_return_journey': bus.bus_num_adults_male_return_journey,
	                 'bus_num_adults_female_return_journey': bus.bus_num_adults_female_return_journey,
	                 'everyone_dropped_off_flag': bus.everyone_dropped_off_flag,
	                 'everyone_dropped_off_time': str(bus.everyone_dropped_off_time),
	                 'feedback_form_taken_from_ngo_flag': bus.feedback_form_taken_from_ngo_flag,
	                 'feedback_form_taken_from_ngo_time': str(bus.feedback_form_taken_from_ngo_time),
	                 'bus_furthest_screen': bus.bus_furthest_screen
	                 }
	return bus_data_dict


# Screen 5 total people picked after last checkpoint
@csrf_exempt
def screen5_total_people_picked(request):
	bus_code_num, volunteer_phone_num = get_bus_phone(request)
	bus_num_children_male_pickedup = request_obtain(request, 'bus_num_children_male_pickedup')
	bus_num_children_female_pickedup = request_obtain(request, 'bus_num_children_female_pickedup')
	bus_num_adults_male_pickedup = request_obtain(request, 'bus_num_adults_male_pickedup')
	bus_num_adults_female_pickedup = request_obtain(request, 'bus_num_adults_female_pickedup')
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_num_children_male_pickedup', bus_num_children_male_pickedup)
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_num_children_female_pickedup', bus_num_children_female_pickedup)
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_num_adults_male_pickedup', bus_num_adults_male_pickedup)
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_num_adults_female_pickedup', bus_num_adults_female_pickedup)
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_furthest_screen', 5)
	return HttpResponse("OK")  # There is no need to return complete bus data for screens 2-12.


# Screen 6 total people picked after last checkpoint
@csrf_exempt
def screen6_everyone_deboarded(request):
	bus_code_num, volunteer_phone_num = get_bus_phone(request)
	save_bus_param(bus_code_num, volunteer_phone_num, 'all_deboarded_at_stadium_flag', True)
	save_bus_param(bus_code_num, volunteer_phone_num, 'all_deboarded_at_stadium_time', timezone.now())  # UTC time
	save_bus_param(bus_code_num, volunteer_phone_num, 'bus_furthest_screen', 6)
	return HttpResponse("OK")  # There is no need to return complete bus data for screens 2-12.

