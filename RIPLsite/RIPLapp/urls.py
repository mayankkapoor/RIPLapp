from django.conf.urls import url

urlpatterns = [  # Examples:  # url(r'^$', 'RIPLsite.views.home', name='home'),
                 url(r'screen1/$', 'RIPLapp.views.screen1login_response', name='screen1'),
                 url(r'screen2/$', 'RIPLapp.views.screen2bus_safe_response', name='screen2'),
                 url(r'screen3/$', 'RIPLapp.views.screen3bus_supply_count', name='screen3'),
                 url(r'screen4/$', 'RIPLapp.views.screen4bus_started_depot', name='screen4'),
                 url(r'screen5/$', 'RIPLapp.views.screen5_total_people_picked', name='screen5'),
                 url(r'screentest/$', 'RIPLapp.views.screentest', name='screentest')

]
