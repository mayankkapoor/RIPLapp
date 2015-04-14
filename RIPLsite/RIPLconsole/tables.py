import django_tables2 as tables
from RIPLapp.models import Volunteer, SOS
from django.utils.safestring import mark_safe


class SOSTable(tables.Table):
	def render_sos_bus(self, value):
		return mark_safe('<span style="background-color: red">%s</span>' % value);

	def render_sos_volunteer(self, value):
		return mark_safe('<span style="background-color: red">%s</span>' % value);

	def render_sos_raise_time(self, value):
		return mark_safe('<span style="background-color: red">%s</span>' % value);

	class Meta:
		model = SOS
		# add class="paleblue" to <table> tag
		attrs = {"class": "paleblue"}


# Fundamentally _expected_number_of_adultshe root of all ForeignKeys comes from Volunteers, so using that as the base model
# for the table and deriving all the associated Bus properties via the ForeignKey 'accessor'
class OperatorConsoleTable(tables.Table):
        bus_depot_zone = tables.Column(accessor='volunteer_bus.bus_depot.depot_zone')
        bus_depot_code = tables.Column(accessor='volunteer_bus.bus_depot.depot_code')
        bus_depot_name = tables.Column(accessor='volunteer_bus.bus_depot.depot_name')
	#bus_safe_flag = tables.Column(accessor='volunteer_bus.bus_safe_flag')
	bus_safe_time = tables.Column(accessor='volunteer_bus.bus_safe_time')
	bus_expected_number_of_children = tables.Column(accessor='volunteer_bus.bus_expected_number_of_children')
	bus_expected_number_of_adults = tables.Column(accessor='volunteer_bus.bus_expected_number_of_adults')
	bus_number_water_bottles_initial = tables.Column(accessor='volunteer_bus.bus_number_water_bottles_initial')
	bus_number_food_packets_initial = tables.Column(accessor='volunteer_bus.bus_number_food_packets_initial')
	bus_number_tickets_initial = tables.Column(accessor='volunteer_bus.bus_number_tickets_initial')
	#bus_started_from_depot_flag = tables.Column(accessor='volunteer_bus.bus_started_from_depot_flag')
	bus_started_from_depot_time = tables.Column(accessor='volunteer_bus.bus_started_from_depot_time')
	#bus_first_aid_kit_available_flag = tables.Column(accessor='volunteer_bus.bus_first_aid_kit_available_flag')
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
	bus_last_location_latitude = tables.Column(accessor='volunteer_bus.bus_last_location_latitude')
	bus_last_location_longitude = tables.Column(accessor='volunteer_bus.bus_last_location_longitude')

	# Render Bus Code Number
	def render_volunteer_bus(self, value):
		return value.bus_code_num
        
       	# Ensure number of children expected == number of children pickedup
	def render_bus_num_children_male_pickedup(self, value, record):
		if record.volunteer_bus.bus_num_children_female_pickedup is None or record.volunteer_bus.bus_expected_number_of_children is None:
			return value

		if value + record.volunteer_bus.bus_num_children_female_pickedup != record.volunteer_bus.bus_expected_number_of_children:
			return mark_safe('<span style="background-color: red">%s</span>' % value)

		else:
			return value

        def render_bus_num_children_female_pickedup(self, value, record):
                if record.volunteer_bus.bus_num_children_male_pickedup is None or record.volunteer_bus.bus_expected_number_of_children is None:
                        return value

                if value + record.volunteer_bus.bus_num_children_male_pickedup != record.volunteer_bus.bus_expected_number_of_children:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

	# Ensure number of adults expected == number of adults picked up
        def render_bus_num_adults_male_pickedup(self, value, record):
                if record.volunteer_bus.bus_num_adults_female_pickedup is None or record.volunteer_bus.bus_expected_number_of_adults is None:
                        return value

                if value + record.volunteer_bus.bus_num_adults_female_pickedup != record.volunteer_bus.bus_expected_number_of_adults:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

        def render_bus_num_adults_female_pickedup(self, value, record):
                if record.volunteer_bus.bus_num_adults_male_pickedup is None or record.volunteer_bus.bus_expected_number_of_adults is None:
                        return value

                if value + record.volunteer_bus.bus_num_adults_male_pickedup != record.volunteer_bus.bus_expected_number_of_adults:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

	# Ensure number of children expected == number of children seated
        def render_num_children_male_seated(self, value, record):
                if record.volunteer_bus.num_children_female_seated is None or record.volunteer_bus.bus_expected_number_of_children is None:
                        return value

                if value + record.volunteer_bus.num_children_female_seated != record.volunteer_bus.bus_expected_number_of_children:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

        def render_num_children_female_seated(self, value, record):
                if record.volunteer_bus.num_children_male_seated is None or record.volunteer_bus.bus_expected_number_of_children is None:
                        return value

                if value + record.volunteer_bus.num_children_male_seated != record.volunteer_bus.bus_expected_number_of_children:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

        # Ensure number of adults expected == number of adults seated
        def render_num_adults_male_seated(self, value, record):
                if record.volunteer_bus.num_adults_female_seated is None or record.volunteer_bus.bus_expected_number_of_adults is None:
                        return value

                if value + record.volunteer_bus.num_adults_female_seated != record.volunteer_bus.bus_expected_number_of_adults:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

        def render_num_adults_female_seated(self, value, record):
                if record.volunteer_bus.num_adults_male_seated is None or record.volunteer_bus.bus_expected_number_of_adults is None:
                        return value

                if value + record.volunteer_bus.num_adults_male_seated != record.volunteer_bus.bus_expected_number_of_adults:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

        # Ensure number of children expected == number of children on return journey
        def render_bus_num_children_male_return_journey(self, value, record):
                if record.volunteer_bus.bus_num_children_female_return_journey is None or record.volunteer_bus.bus_expected_number_of_children is None:
                        return value

                if value + record.volunteer_bus.bus_num_children_female_return_journey != record.volunteer_bus.bus_expected_number_of_children:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

        def render_bus_num_children_female_return_journey(self, value, record):
                if record.volunteer_bus.bus_num_children_male_return_journey is None or record.volunteer_bus.bus_expected_number_of_children is None:
                        return value

                if value + record.volunteer_bus.bus_num_children_male_return_journey != record.volunteer_bus.bus_expected_number_of_children:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

        # Ensure number of adults expected == number of adults on return journey
        def render_bus_num_adults_male_return_journey(self, value, record):
                if record.volunteer_bus.bus_num_adults_female_return_journey is None or record.volunteer_bus.bus_expected_number_of_adults is None:
                        return value

                if value + record.volunteer_bus.bus_num_adults_female_return_journey != record.volunteer_bus.bus_expected_number_of_adults:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

        def render_bus_num_adults_female_return_journey(self, value, record):
                if record.volunteer_bus.bus_num_adults_male_return_journey is None or record.volunteer_bus.bus_expected_number_of_adults is None:
                        return value

                if value + record.volunteer_bus.bus_num_adults_male_return_journey != record.volunteer_bus.bus_expected_number_of_adults:
                        return mark_safe('<span style="background-color: red">%s</span>' % value)

                else:
                        return value

	# Ensure number of tickets == number of children + adult expected
	def render_bus_number_tickets_initial(self, value, record):
		if record.volunteer_bus.bus_expected_number_of_adults is None or record.volunteer_bus.bus_expected_number_of_children is None:
			return value

		if record.volunteer_bus.bus_expected_number_of_adults + record.volunteer_bus.bus_expected_number_of_children != value:
			return mark_safe('<span style="background-color: red">%s</span>' % value)

		else:
			return value

	class Meta:
		model = Volunteer
		# add class="paleblue" to <table> tag
		attrs = {"class": "paleblue"}
		sequence = ("volunteer_bus", "...")
