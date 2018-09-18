from django.conf.urls import url, include
from .serializers import router
from .views import index
from django.http import HttpResponse

urlpatterns = [
	url(r'^api/', include(router.urls)),
	url(r'index/', index),
]
