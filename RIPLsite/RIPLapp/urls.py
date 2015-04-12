from django.conf.urls import url

urlpatterns = [  # Examples:  # url(r'^$', 'RIPLsite.views.home', name='home'),
                 url(r'screen1/$', 'RIPLapp.views.screen1login_response', name='screen1'),
                 url(r'screen2/$', 'RIPLapp.views.screen2bus_safe_response', name='screen2'),
                 url(r'screen3/$', 'RIPLapp.views.screen3bus_supply_count', name='screen3'),
                 url(r'screen4/$', 'RIPLapp.views.screen4bus_started_depot', name='screen4'),
                 url(r'screen5/$', 'RIPLapp.views.screen5_total_people_picked', name='screen5'),
                 url(r'screentest/$', 'RIPLapp.views.screentest', name='screentest'),
                 url(r'screen6/$', 'RIPLapp.views.screen6_everyone_deboarded', name='screen6'),
                 url(r'screen7/$', 'RIPLapp.views.screen7_seated_at_stadium_count', name='screen7'),
                 url(r'screen8/$', 'RIPLapp.views.screen8_seated_for_return_journey', name='screen8'),
                 url(r'screen9/$', 'RIPLapp.views.screen9_everyone_deboarded_final', name='screen9'),
                 url(r'screen10/$', 'RIPLapp.views.screen10_submitted_ngo_form', name='screen10'),
                 url(r'sos/$', 'RIPLapp.views.sos_report', name='sos_report'),
                 url(r'location/$', 'RIPLapp.views.location_report', name='location_report'),

                 ]
