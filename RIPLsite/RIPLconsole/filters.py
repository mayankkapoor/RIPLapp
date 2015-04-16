import django_filters
from RIPLapp.models import SOS, Volunteer

class VolunteerFilter(django_filters.FilterSet):
        class Meta:
                model = Volunteer
                fields = ['volunteer_bus__bus_depot__depot_zone']

class SOSFilter(django_filters.FilterSet):
        class Meta:
                model = SOS
                fields = ['sos_bus__bus_depot__depot_zone']
