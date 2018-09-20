from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet

from .models import Clinitian

router = DefaultRouter()

class ClinitianSerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= Clinitian
		fields = ('user', 'email', 'first_name', 'last_name', 'contact', 'unique_id', 'HealthCare')
		read_only_fields = ('user','email', 'HealthCare')

class ClinitianViewset(viewsets.ModelViewSet):
	"""ClinitianViewset for REST Endpoint"""
	serializer_class 	= ClinitianSerializer
	queryset 			= Clinitian.objects.all()
	
router.register(r'phc_emp', ClinitianViewset)

router.register(r'devices', FCMDeviceViewSet)
router.register(r'authdevices', FCMDeviceAuthorizedViewSet)