from django.db import models

# Create your models here.


class Depot(models.Model):
	depot_zone = models.IntegerField()
	depot_code = models.CharField(max_length=32, primary_key=True)
	depot_name = models.CharField(max_length=99, blank=False, null=False)

	def __unicode__(self):  # __unicode__ on Python 2
		return u'%s' % self.depot_code


class Bus(models.Model):
	bus_code_num = models.CharField(max_length=20,
	                                primary_key=True)  # TODO: Is setting using bus_code_num as primary_key correct? There may be two rows with same bus number but different volunteers
	bus_safe_flag = models.IntegerField(null=True, blank=True)
	bus_safe_time = models.DateTimeField(null=True, blank=True)  # UTC time
	bus_expected_number_of_children = models.IntegerField(null=True, blank=True)
	bus_expected_number_of_adults = models.IntegerField(null=True, blank=True)
	bus_number_water_bottles_initial = models.IntegerField(null=True, blank=True)
	bus_number_food_packets_initial = models.IntegerField(null=True, blank=True)
	bus_number_tickets_initial = models.IntegerField(null=True, blank=True)
	bus_started_from_depot_flag = models.IntegerField(null=True, blank=True)
	bus_started_from_depot_time = models.DateTimeField(null=True, blank=True)  # UTC time
	bus_first_aid_kit_available_flag = models.IntegerField(null=True, blank=True)
	bus_num_children_male_pickedup = models.IntegerField(null=True, blank=True)
	bus_num_children_female_pickedup = models.IntegerField(null=True, blank=True)
	bus_num_adults_male_pickedup = models.IntegerField(null=True, blank=True)
	bus_num_adults_female_pickedup = models.IntegerField(null=True, blank=True)
	all_deboarded_at_stadium_flag = models.IntegerField(null=True, blank=True)
	all_deboarded_at_stadium_time = models.DateTimeField(null=True, blank=True)
	num_children_male_seated = models.IntegerField(null=True, blank=True)
	num_children_female_seated = models.IntegerField(null=True, blank=True)
	num_adults_male_seated = models.IntegerField(null=True, blank=True)
	num_adults_female_seated = models.IntegerField(null=True, blank=True)
	bus_num_children_male_return_journey = models.IntegerField(null=True, blank=True)
	bus_num_children_female_return_journey = models.IntegerField(null=True, blank=True)
	bus_num_adults_male_return_journey = models.IntegerField(null=True, blank=True)
	bus_num_adults_female_return_journey = models.IntegerField(null=True, blank=True)
	everyone_dropped_off_flag = models.IntegerField(null=True, blank=True)
	everyone_dropped_off_time = models.DateTimeField(null=True, blank=True)  # UTC time
	feedback_form_taken_from_ngo_flag = models.IntegerField(null=True, blank=True)
	feedback_form_taken_from_ngo_time = models.DateTimeField(null=True, blank=True)  # UTC time
	bus_depot = models.ForeignKey(Depot, null=True, blank=True)
	bus_furthest_screen = models.IntegerField(null=True, blank=True)
	bus_last_location_latitude = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10, default=None)
	bus_last_location_longitude = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10, default=None)

	def __unicode__(self):  # __unicode__ on Python 2
		return u'%s-%s' % (self.bus_code_num, self.volunteer_set.all())


class Volunteer(models.Model):
	volunteer_phone_num = models.BigIntegerField(primary_key=True)
	volunteer_full_name = models.CharField(max_length=200, null=True, blank=True)
	volunteer_bus = models.ForeignKey(Bus, null=False)

	def __unicode__(self):  # __unicode__ on Python 2
		return u'%s' % self.volunteer_phone_num


class SOS(models.Model):
	sos_bus = models.ForeignKey(Bus)
	sos_volunteer = models.ForeignKey(Volunteer)
	sos_raise_time = models.DateTimeField(null=False, blank=False)

	def __unicode__(self):  # __unicode__ on Python 2
		sos_string = str(self.sos_bus) + "-" + str(self.sos_volunteer) + "-" + str(self.sos_raise_time)
		return u'%s' % sos_string
