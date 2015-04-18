import random
import decimal

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import yaml
from django.utils import timezone

from RIPLapp.views import *
from RIPLapp.models import Bus, Volunteer
from RIPLsite import settings

# Create your tests here.

time_now = timezone.now()


class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)


class Screen1LoginTest(TestCase):
	def test_url_resolves_to_screen1_view(self):
		found = resolve(settings.APP_URL + '/screen1/')
		self.assertEqual(found.func, screen1login_response)

	def test_screen1_saves_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus', bus_expected_number_of_children=1)
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)

		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		# print response

		self.assertContains(response, 'correct_bus')
		self.assertNotContains(response, 'other_bus')
		self.assertContains(response, '1111111111')
		self.assertNotContains(response, '2222222222')


class Screen2BusSafeTest(TestCase):
	def test_url_resolves_to_screen2_view(self):
		found = resolve(settings.APP_URL + '/screen2/')
		self.assertEqual(found.func, screen2bus_safe_response)

	def test_screen2_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		screen_vars = {'bus_safe_flag': 0,
		               'bus_safe_time': time_now,
		               'bus_last_location_latitude': 0.0,
		               'bus_last_location_longitude': 0.0,
		               'bus_furthest_screen': 2
		               }
		for key in screen_vars:
			if 'num' in key:
				correct_bus_dict.update({key: random.randint(1, 100)})
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})
		response = self.client.post(settings.APP_URL + '/screen2/', correct_bus_dict)
		self.assertContains(response, 'OK')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class Screen3BusSupplyCountTest(TestCase):
	def test_url_resolves_to_screen3_view(self):
		found = resolve(settings.APP_URL + '/screen3/')
		self.assertEqual(found.func, screen3bus_supply_count)

	def test_screen3_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		screen_vars = {'bus_number_water_bottles_initial': 0,
		               'bus_number_food_packets_initial': 0,
		               'bus_number_tickets_initial': 0,
		               'bus_first_aid_kit_available_flag': 0,  # 'everyone_dropped_off_flag':0,
		               'bus_last_location_latitude': 0.0,
		               'bus_last_location_longitude': 0.0,
		               'bus_furthest_screen': 3
		               }
		for key in screen_vars:
			if 'number' in key:
				correct_bus_dict.update({key: random.randint(1, 100)})
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})
		response = self.client.post(settings.APP_URL + '/screen3/', correct_bus_dict)
		self.assertContains(response, 'OK')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class Screen4BusdepotstartedTest(TestCase):
	def test_url_resolves_to_screen3_view(self):
		found = resolve(settings.APP_URL + '/screen4/')
		self.assertEqual(found.func, screen4bus_started_depot)

	def test_screen4_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		time_now = timezone.now()
		screen_vars = {'bus_started_from_depot_flag': 0,
		               'bus_started_from_depot_time': time_now,
		               'bus_last_location_latitude': 0.0,
		               'bus_last_location_longitude': 0.0,
		               'bus_furthest_screen': 4
		               }
		for key in screen_vars:
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})
		response = self.client.post(settings.APP_URL + '/screen4/', correct_bus_dict)
		self.assertContains(response, 'OK')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class Screen5TotalPeoplePickedTest(TestCase):
	def test_url_resolves_to_screen1_view(self):
		found = resolve(settings.APP_URL + '/screen5/')
		self.assertEqual(found.func, screen5_total_people_picked)

	def test_screen5_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		screen_vars = {'bus_num_children_male_pickedup': 0,
		               'bus_num_children_female_pickedup': 0,
		               'bus_num_adults_male_pickedup': 0,
		               'bus_num_adults_female_pickedup': 0,
		               'bus_last_location_latitude': 0.0,
		               'bus_last_location_longitude': 0.0,
		               'bus_furthest_screen': 5
		               }
		for key in screen_vars:
			if 'num' in key:
				correct_bus_dict.update({key: random.randint(1, 100)})
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})
		response = self.client.post(settings.APP_URL + '/screen5/', correct_bus_dict)
		self.assertContains(response, 'OK')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class Screen6EveryoneDeboardedTest(TestCase):
	def test_url_resolves_to_screen6_view(self):
		found = resolve(settings.APP_URL + '/screen6/')
		self.assertEqual(found.func, screen6_everyone_deboarded)

	def test_screen6_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		screen6_vars = {'all_deboarded_at_stadium_flag': 0,
		                'all_deboarded_at_stadium_time': time_now,
		                'bus_last_location_latitude': 0.0,
		                'bus_last_location_longitude': 0.0,
		                'bus_furthest_screen': 6
		                }
		for key in screen6_vars:
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})
		response = self.client.post(settings.APP_URL + '/screen6/', correct_bus_dict)
		self.assertContains(response, 'bus_num_children_male_pickedup')
		self.assertContains(response, 'bus_num_children_female_pickedup')
		self.assertContains(response, 'bus_num_adults_male_pickedup')
		self.assertContains(response, 'bus_num_adults_female_pickedup')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen6_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class SOSTest(TestCase):
	def test_url_resolves_to_sos_view(self):
		found = resolve(settings.APP_URL + '/sos/')
		self.assertEqual(found.func, sos_report)

	def test_sos_saves_properly(self):
		correct_bus = Bus.objects.create(bus_code_num='correct_bus')
		correct_volunteer = Volunteer.objects.create(volunteer_bus=correct_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# correct_sos = SOS.objects.create(sos_bus=correct_bus, sos_volunteer=correct_volunteer, sos_raise_time=timezone.now())
		# other_sos = SOS.objects.create(sos_bus=other_bus, sos_volunteer=other_volunteer, sos_raise_time=timezone.now())

		response = self.client.post(settings.APP_URL + '/sos/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})

		self.assertContains(response, "correct_bus")
		self.assertContains(response, "1111111111")
		self.assertContains(response, "saved at")
		self.assertNotContains(response, "other_bus")
		self.assertNotContains(response, "2222222222")


class Screen7SeatedAtStadiumTest(TestCase):
	def test_url_resolves_to_screen7_view(self):
		found = resolve(settings.APP_URL + '/screen7/')
		self.assertEqual(found.func, screen7_seated_at_stadium_count)

	def test_screen7_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		screen_vars = {'num_children_male_seated': 0,
		               'num_children_female_seated': 0,
		               'num_adults_male_seated': 0,
		               'num_adults_female_seated': 0,
		               'bus_last_location_latitude': 0.0,
		               'bus_last_location_longitude': 0.0,
		               'bus_furthest_screen': 7
		               }
		for key in screen_vars:
			if 'num' in key:
				correct_bus_dict.update({key: random.randint(1, 100)})
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})

		response = self.client.post(settings.APP_URL + '/screen7/', correct_bus_dict)
		self.assertContains(response, 'bus_num_children_male_pickedup')
		self.assertContains(response, 'bus_num_children_female_pickedup')
		self.assertContains(response, 'bus_num_adults_male_pickedup')
		self.assertContains(response, 'bus_num_adults_female_pickedup')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class Screen8SeatedReturnJourneyTest(TestCase):
	def test_url_resolves_to_screen8_view(self):
		found = resolve(settings.APP_URL + '/screen8/')
		self.assertEqual(found.func, screen8_seated_for_return_journey)

	def test_screen8_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		screen_vars = {'bus_num_children_male_return_journey': 0,
		               'bus_num_children_female_return_journey': 0,
		               'bus_num_adults_male_return_journey': 0,
		               'bus_num_adults_female_return_journey': 0,
		               'bus_last_location_latitude': 0.0,
		               'bus_last_location_longitude': 0.0,
		               'bus_furthest_screen': 8
		               }
		for key in screen_vars:
			if 'num' in key:
				correct_bus_dict.update({key: random.randint(1, 100)})
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})

		response = self.client.post(settings.APP_URL + '/screen8/', correct_bus_dict)
		self.assertContains(response, 'OK')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class Screen9EveryoneDeboardedTest(TestCase):
	def test_url_resolves_to_screen_view(self):
		found = resolve(settings.APP_URL + '/screen9/')
		self.assertEqual(found.func, screen9_everyone_deboarded_final)

	def test_screen9_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		screen_vars = {'everyone_dropped_off_flag': 0,
		               'everyone_dropped_off_time': time_now,
		               'bus_last_location_latitude': 0.0,
		               'bus_last_location_longitude': 0.0,
		               'bus_furthest_screen': 9
		               }
		for key in screen_vars:
			if 'num' in key:
				correct_bus_dict.update({key: random.randint(1, 100)})
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})

		response = self.client.post(settings.APP_URL + '/screen9/', correct_bus_dict)
		self.assertContains(response, 'OK')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class Screen10SubmitNGOFormTest(TestCase):
	def test_url_resolves_to_screen_view(self):
		found = resolve(settings.APP_URL + '/screen10/')
		self.assertEqual(found.func, screen10_submitted_ngo_form)

	def test_screen10_saves_to_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus')
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# It first needs to go to screen1 for creating the bus
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		self.assertContains(response, 'correct_bus')
		response = self.client.post(settings.APP_URL + '/screen1/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		self.assertContains(response, 'other_bus')
		correct_bus_dict = {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111}
		screen_vars = {'feedback_form_taken_from_ngo_flag': 0,
		               'feedback_form_taken_from_ngo_time': time_now,
		               'bus_last_location_latitude': 0.0,
		               'bus_last_location_longitude': 0.0,
		               'bus_furthest_screen': 10
		               }
		for key in screen_vars:
			if 'num' in key:
				correct_bus_dict.update({key: random.randint(1, 100)})
			if 'flag' in key:
				correct_bus_dict.update({key: random.randint(0, 1)})
			if 'location' in key:
				correct_bus_dict.update({key: decimal.Decimal(random.randrange(-900000, 900000, 1)) / 10000})

		response = self.client.post(settings.APP_URL + '/screen10/', correct_bus_dict)
		self.assertContains(response, 'OK')
		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})
		response_yaml = yaml.load(response.content)
		for key in correct_bus_dict:
			if 'location' in key:
				self.assertEqual(decimal.Decimal(response_yaml[key]), decimal.Decimal(correct_bus_dict[key]))
			else:
				self.assertEqual(str(response_yaml[key]), str(correct_bus_dict[key]))

		response = self.client.post(settings.APP_URL + '/screentest/',
		                            {'bus_code_num': 'other_bus', 'volunteer_phone_num': 2222222222})
		response_yaml = yaml.load(response.content)
		for key in screen_vars:
			self.assertEqual(str(response_yaml[key]), str(None))


class LocationTest(TestCase):
	def test_url_resolves_to_location_view(self):
		found = resolve(settings.APP_URL + '/location/')
		self.assertEqual(found.func, location_report)

	def test_location_saves_properly(self):
		correct_bus = Bus.objects.create(bus_code_num='correct_bus')
		correct_volunteer = Volunteer.objects.create(volunteer_bus=correct_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)
		# correct_sos = SOS.objects.create(sos_bus=correct_bus, sos_volunteer=correct_volunteer, sos_raise_time=timezone.now())
		# other_sos = SOS.objects.create(sos_bus=other_bus, sos_volunteer=other_volunteer, sos_raise_time=timezone.now())

		response = self.client.post(settings.APP_URL + '/location/',
		                            {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111,
		                             'bus_last_location_latitude': 45.23, 'bus_last_location_longitude': -175.3456})

		self.assertContains(response, "45.23")
		self.assertContains(response, "-175.3456")
