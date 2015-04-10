from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'RIPLsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'RIPLapp.views.home_page', name='home_page'),
    url(r'^app/', include('RIPLapp.urls')),
    url(r'^console/', include('RIPLconsole.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
]
