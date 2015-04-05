from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sys, json

from RIPLapp.models import Volunteer, Bus

# Create your views here.


def home_page(request):
	context = {}
	return render(request, 'home.html', context)


# function that returns JSON response for login screen
@csrf_exempt
def screen1login_response(request):
	bus_code_num = request.POST.get('bus_code_num', None)
	volunteer_phone_num = request.POST.get('volunteer_phone_num', None)
	if bus_code_num and volunteer_phone_num:
		response_data = response_data_dict(bus_code_num, volunteer_phone_num)
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		return HttpResponse("Either bus_code_num or volunteer_phone_num doesn't exist in your POST request.")


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
			bus_data_dict = turn_bus_data_into_dict(bus)
			# print bus_data_dict
		else:
			print "Error! More than 1 buses returned for given bus code and volunteer phone number. Should not be " \
			      "possible. Buses: ", query_buses
		return bus_data_dict
	except Exception, e:
		print 'Oops, %s did not complete. Exception: %s' % (sys._getframe().f_code.co_name, e)


# Encapsulating mainly for DRY later.
def turn_bus_data_into_dict(bus):
	bus_data_dict = {'bus_safe_flag': bus.bus_safe_flag, 'bus_safe_time': bus.bus_safe_time,
	                 'bus_expected_number_of_children': bus.bus_expected_number_of_children,
	                 'bus_expected_number_of_adults': bus.bus_expected_number_of_adults,
	                 'bus_number_food_packets_initial': bus.bus_number_food_packets_initial,
	                 'bus_number_water_bottles_initial': bus.bus_number_water_bottles_initial,
	                 'bus_started_from_depot_flag': bus.bus_started_from_depot_flag,
	                 'bus_started_from_depot_time': bus.bus_started_from_depot_time
	                 }
	return bus_data_dict
