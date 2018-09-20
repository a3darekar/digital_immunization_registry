from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet

from .models import Clinitian

router = DefaultRouter()

class ClinitianSerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= Clinitian
		fields = ('user', 'email', 'first_name', 'last_name', 'contact', 'unique_id', 'HealthCare')



class ClinitianViewset(viewsets.ModelViewSet):
	"""ClinitianViewset for REST Endpoint"""
	serializer_class = ClinitianSerializer
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			return Clinitian.objects.get(user = user)
		else:
			return Clinitian.objects.none()


router.register(r'phc_emp', ClinitianViewset, base_name = 'clinitian-details')

router.register(r'devices', FCMDeviceViewSet)
router.register(r'authdevices', FCMDeviceAuthorizedViewSet)