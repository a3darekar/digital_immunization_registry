from django.conf.urls import url, include

from .views import router
from .views import index, schedule_vaccines, GeneratePdf

urlpatterns = [
    url(r'^reports/', GeneratePdf.as_view(), name='schedule_pdf'),
	url(r'^api/', include(router.urls)),
	url(r'index/', index),
	url(r'api/schedule_vaccines/', schedule_vaccines),
]
