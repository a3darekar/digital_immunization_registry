from django.conf.urls import url, include
from django.contrib.auth.views import login

urlpatterns = [
	url(r'^api/', include('rest_auth.urls')),
	url(r'^api/register/', include('rest_auth.registration.urls')),
	url(r'^login/$', login),
]
