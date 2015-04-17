import django_tables2 as tables
from RIPLapp.models import Volunteer, SOS
from django.utils.safestring import mark_safe
from django.utils import timezone

def highlightValue(value):
	return mark_safe('<span style="background-color: yellow">%s</span>' % value)

def verifySumConstraint(value, addend, expectedSum):
	if value is None or addend is None or expectedSum is None:
		return value

	if value + addend != expectedSum:
		return highlightValue(value)
	else:
		return value

class SOSTable(tables.Table):
	volunteer_full_name = tables.Column(accessor='sos_volunteer.volunteer_full_name')

	def render_sos_bus(self, value):
		return highlightValue(value.bus_code_num)

	def render_sos_volunteer(self, value):
		return highlightValue(value)

	def render_sos_raise_time(self, value):
		return highlightValue(timezone.localtime(value))

	def render_volunteer_full_name(self, value):
		return highlightValue(value)

	class Meta:
		model = SOS
		# add class="paleblue" to <table> tag
		attrs = {"class": "paleblue"}
		sequence = ("...", "sos_bus", "sos_volunteer", "volunteer_full_name", "sos_raise_time")


# Fundamentally the root of all ForeignKeys comes from Volunteers, so using that as the base model
# for the table and deriving all the associated Bus properties via the ForeignKey 'accessor'
class OperatorConsoleTable(tables.Table):
	bus_depot_zone = tables.Column(accessor='volunteer_bus.bus_depot.depot_zone')
	bus_depot_code = tables.Column(accessor='volunteer_bus.bus_depot.depot_code')
	bus_depot_name = tables.Column(accessor='volunteer_bus.bus_depot.depot_name')
	bus_volunteer_depot_login_time = tables.Column(accessor='volunteer_bus.bus_volunteer_depot_login_time')
	bus_safe_time = tables.Column(accessor='volunteer_bus.bus_safe_time')
	bus_expected_number_of_children = tables.Column(accessor='volunteer_bus.bus_expected_number_of_children')
	bus_expected_number_of_adults = tables.Column(accessor='volunteer_bus.bus_expected_number_of_adults')
	bus_number_water_bottles_initial = tables.Column(accessor='volunteer_bus.bus_number_water_bottles_initial')
	bus_number_food_packets_initial = tables.Column(accessor='volunteer_bus.bus_number_food_packets_initial')
	bus_number_tickets_initial = tables.Column(accessor='volunteer_bus.bus_number_tickets_initial')
	#bus_started_from_depot_flag = tables.Column(accessor='volunteer_bus.bus_started_from_depot_flag')
	bus_started_from_depot_time = tables.Column(accessor='volunteer_bus.bus_started_from_depot_time')
	bus_first_aid_kit_available_flag = tables.Column(accessor='volunteer_bus.bus_first_aid_kit_available_flag')
	bus_num_children_male_pickedup = tables.Column(accessor='volunteer_bus.bus_num_children_male_pickedup')
	bus_num_children_female_pickedup = tables.Column(accessor='volunteer_bus.bus_num_children_female_pickedup')
	bus_num_adults_male_pickedup = tables.Column(accessor='volunteer_bus.bus_num_adults_male_pickedup')
	bus_num_adults_female_pickedup = tables.Column(accessor='volunteer_bus.bus_num_adults_female_pickedup')
	#all_deboarded_at_stadium_flag = tables.Column(accessor='volunteer_bus.all_deboarded_at_stadium_flag')
	all_deboarded_at_stadium_time = tables.Column(accessor='volunteer_bus.all_deboarded_at_stadium_time')
	num_children_male_seated = tables.Column(accessor='volunteer_bus.num_children_male_seated')
	num_children_female_seated = tables.Column(accessor='volunteer_bus.num_children_female_seated')
	num_adults_male_seated = tables.Column(accessor='volunteer_bus.num_adults_male_seated')
	num_adults_female_seated = tables.Column(accessor='volunteer_bus.num_adults_female_seated')
	bus_num_children_male_return_journey = tables.Column(accessor='volunteer_bus.bus_num_children_male_return_journey')
	bus_num_children_female_return_journey = tables.Column(
		accessor='volunteer_bus.bus_num_children_female_return_journey')
	bus_num_adults_male_return_journey = tables.Column(accessor='volunteer_bus.bus_num_adults_male_return_journey')
	bus_num_adults_female_return_journey = tables.Column(accessor='volunteer_bus.bus_num_adults_female_return_journey')
	#everyone_dropped_off_flag = tables.Column(accessor='volunteer_bus.everyone_dropped_off_flag')
	everyone_dropped_off_time = tables.Column(accessor='volunteer_bus.everyone_dropped_off_time')
	#feedback_form_taken_from_ngo_flag = tables.Column(accessor='volunteer_bus.feedback_form_taken_from_ngo_flag')
	feedback_form_taken_from_ngo_time = tables.Column(accessor='volunteer_bus.feedback_form_taken_from_ngo_time')
	bus_furthest_screen = tables.Column(accessor='volunteer_bus.bus_furthest_screen')
	# bus_last_location_latitude = tables.Column(accessor='volunteer_bus.bus_last_location_latitude')
	# bus_last_location_longitude = tables.Column(accessor='volunteer_bus.bus_last_location_longitude')

	# Render Bus Code Number
	def render_volunteer_bus(self, value):
		return value.bus_code_num
	
	# Ensure number of children expected == number of children picked up
	def render_bus_num_children_male_pickedup(self, value, record):
		return verifySumConstraint(value, 
					record.volunteer_bus.bus_num_children_female_pickedup, 
					record.volunteer_bus.bus_expected_number_of_children)

	def render_bus_num_children_female_pickedup(self, value, record):
                return verifySumConstraint(value,
                                        record.volunteer_bus.bus_num_children_male_pickedup, 
                                        record.volunteer_bus.bus_expected_number_of_children)

	# Ensure number of adults expected == number of adults picked up
	def render_bus_num_adults_male_pickedup(self, value, record):
                return verifySumConstraint(value,
                                        record.volunteer_bus.bus_num_adults_female_pickedup, 
                                        record.volunteer_bus.bus_expected_number_of_adults)
		
	def render_bus_num_adults_female_pickedup(self, value, record):
		return verifySumConstraint(value,
                                        record.volunteer_bus.bus_num_adults_male_pickedup,  
                                        record.volunteer_bus.bus_expected_number_of_adults)

	# Ensure number of children expected == number of children seated
	def render_num_children_male_seated(self, value, record):
		return verifySumConstraint(value,
                                        record.volunteer_bus.num_children_female_seated,  
                                        record.volunteer_bus.bus_expected_number_of_children)

	def render_num_children_female_seated(self, value, record):
		return verifySumConstraint(value,
                                        record.volunteer_bus.num_children_male_seated,  
                                        record.volunteer_bus.bus_expected_number_of_children)	

	# Ensure number of adults expected == number of adults seated
	def render_num_adults_male_seated(self, value, record):
		return verifySumConstraint(value,
                                        record.volunteer_bus.num_adults_female_seated,  
                                        record.volunteer_bus.bus_expected_number_of_adults)

	def render_num_adults_female_seated(self, value, record):
		return verifySumConstraint(value,
                                        record.volunteer_bus.num_adults_male_seated,  
                                        record.volunteer_bus.bus_expected_number_of_adults)

	# Ensure number of children expected == number of children on return journey
	def render_bus_num_children_male_return_journey(self, value, record):
		return verifySumConstraint(value,
                                        record.volunteer_bus.bus_num_children_female_return_journey,  
                                        record.volunteer_bus.bus_expected_number_of_children)

	def render_bus_num_children_female_return_journey(self, value, record):
		return verifySumConstraint(value,
                                        record.volunteer_bus.bus_num_children_male_return_journey,
                                        record.volunteer_bus.bus_expected_number_of_children)

	# Ensure number of adults expected == number of adults on return journey
	def render_bus_num_adults_male_return_journey(self, value, record):
		return verifySumConstraint(value,
                                        record.volunteer_bus.bus_num_adults_female_return_journey,
                                        record.volunteer_bus.bus_expected_number_of_adults)

	def render_bus_num_adults_female_return_journey(self, value, record):
                return verifySumConstraint(value,
                                        record.volunteer_bus.bus_num_adults_male_return_journey,
                                        record.volunteer_bus.bus_expected_number_of_adults)

	# Ensure number of tickets == number of children + adult expected
	def render_bus_number_tickets_initial(self, value, record):
                return verifySumConstraint(value,
                                        record.volunteer_bus.bus_expected_number_of_adults,
                                        record.volunteer_bus.bus_expected_number_of_children)

	class Meta:
		model = Volunteer
		# add class="paleblue" to <table> tag
		attrs = {"class": "paleblue"}
		sequence = ("bus_depot_zone", "bus_depot_code", "bus_depot_name", "volunteer_bus", "...")
