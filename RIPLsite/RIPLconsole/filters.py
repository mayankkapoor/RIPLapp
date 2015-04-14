import django_filters
from RIPLapp.models import Volunteer

class VolunteerFilter(django_filters.FilterSet):
        class Meta:
                model = Volunteer
                fields = ['volunteer_bus__bus_depot__depot_zone']
