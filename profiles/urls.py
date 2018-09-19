from django.conf.urls import url, include

urlpatterns = [
	url(r'^api/', include('rest_auth.urls')),
]
