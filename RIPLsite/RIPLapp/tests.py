from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, JsonResponse
from django.template.loader import render_to_string

from RIPLapp.views import *
from RIPLapp.models import Bus, Volunteer
from RIPLsite import settings

# Create your tests here.


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

	def test_response_data_dict_returns_correct_bus(self):
		new_bus = Bus.objects.create(bus_code_num='correct_bus', bus_expected_number_of_children=1)
		new_volunteer = Volunteer.objects.create(volunteer_bus=new_bus, volunteer_phone_num=1111111111)
		other_bus = Bus.objects.create(bus_code_num='other_bus')
		other_volunteer = Volunteer.objects.create(volunteer_bus=other_bus, volunteer_phone_num=2222222222)

		response = self.client.post(settings.APP_URL + '/screen1/', {'bus_code_num': 'correct_bus', 'volunteer_phone_num': 1111111111})

		self.assertContains(response, 'correct_bus')
		self.assertNotContains(response, 'other_bus')
		self.assertContains(response, '1111111111')
		self.assertNotContains(response, '2222222222')
