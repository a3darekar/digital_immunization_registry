from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^admin/status/', include('celerybeat_status.urls')),
	url(r'^auth/', include('profiles.urls')),
	url(r'^', include('operations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
			static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
