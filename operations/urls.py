from django.conf.urls import url, include
from .serializers import router
from django.http import HttpResponse

from .views import index, ParentList, BabyList, ClinitianList, BabyTagList

urlpatterns = [
	url(r'^api/', include(router.urls)),
	url(r'index/', index),
	url('^parent/', ParentList.as_view()),
	url('^phc_emp/', ClinitianList.as_view()),
	url('^babies/', BabyTagList.as_view()),
	url('^babies/pk/(?P<pk>.+)/$', BabyList.as_view()),
]
