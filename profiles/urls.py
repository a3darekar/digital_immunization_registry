from django.conf.urls import url, include
from django.contrib.auth.views import logout, login


urlpatterns = [
	url(r'^login/$', login, name='login'),
	url(r'^logout/$', logout, name='logout'),
	url(r'^api/', include('rest_auth.urls')),
]
