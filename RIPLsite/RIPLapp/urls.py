from django.conf.urls import url

urlpatterns = [
	# Examples:
	# url(r'^$', 'RIPLsite.views.home', name='home'),
	url(r'screen1/$', 'RIPLapp.views.screen1login_response', name='screen1')

]