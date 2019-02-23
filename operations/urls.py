from django.conf.urls import url, include
from .views import router
from django.http import HttpResponse

from .views import index, schedule_vaccines

urlpatterns = [
	url(r'^api/', include(router.urls)),
	url(r'index/', index),
	url(r'api/schedule_vaccines/', schedule_vaccines),
]
