from django.conf.urls import url

urlpatterns = [  # Examples:  # url(r'^$', 'RIPLsite.views.home', name='home'),
                 url(r'screen1/$', 'RIPLapp.views.screen1login_response', name='screen1'),
                 url(r'screen2/$', 'RIPLapp.views.screen2bus_safe_response', name='screen2'),
                 url(r'screen5/$', 'RIPLapp.views.screen5_total_people_picked', name='screen5'),
                 url(r'screen6/$', 'RIPLapp.views.screen6_everyone_deboarded', name='screen6')

]
