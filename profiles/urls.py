from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('rest_auth.urls')),
    url(r'^api/register/', include('rest_auth.registration.urls')),
    url(r'^', include('allauth.urls')),
]
