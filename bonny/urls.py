from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^auth/', include('profiles.urls')),
	url(r'^', include('operations.urls')),
]
