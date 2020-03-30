from django.conf.urls import url, include
from graphene_django.views import GraphQLView

from .views import router
from .views import index, schedule_vaccines, generatePdf, UserListView

urlpatterns = [
	url(r'^reports/', generatePdf, name='schedule_pdf'),
	url(r'api/schedule_vaccines/', schedule_vaccines),
	url(r'api/users/', UserListView.as_view()),
	url(r'^api/v2/', GraphQLView.as_view(graphiql=True)),
	url(r'^api/', include(router.urls)),
	url(r'^$', index),
]
