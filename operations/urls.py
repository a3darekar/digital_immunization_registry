from django.conf.urls import url, include

from .views import router
from .views import index, schedule_vaccines, generatePdf, UserListView

urlpatterns = [
	url(r'^reports/', generatePdf, name='schedule_pdf'),
	url(r'api/schedule_vaccines/', schedule_vaccines),
	url(r'api/users/', UserListView.as_view()),
	url(r'^api/', include(router.urls)),
	url(r'index/', index),
	url(r'^$', index),
]
