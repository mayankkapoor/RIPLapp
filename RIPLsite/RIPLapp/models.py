from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator

# Create your models here.


class Bus(models.Model):
	bus_code_num = models.CharField(max_length=20, null=False, blank=False)
	bus_safe_flag = models.BooleanField(default=False)
	bus_safe_time = models.DateTimeField(null=True, blank=True)
	bus_expected_number_of_children = models.IntegerField(null=True)
	bus_expected_number_of_adults = models.IntegerField(null=True)
	bus_number_water_bottles_initial = models.IntegerField(null=True)
	bus_number_food_packets_initial = models.IntegerField(null=True)
	bus_started_from_depot_flag = models.BooleanField(default=False)
	bus_started_from_depot_time = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.bus_code_no


class Volunteer(models.Model):
	volunteer_phone_num = models.BigIntegerField(null=False, validators=[MaxLengthValidator(10), MinLengthValidator(10)])
	volunteer_full_name = models.CharField(max_length=200, null=True, blank=True)
	volunteer_bus = models.ForeignKey(Bus)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.volunteer_phone_number
