from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Clinitian, Parent, Baby

router = DefaultRouter()

class ClinitianSerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= Clinitian
		fields  = ('user', 'email', 'first_name', 'last_name', 'contact', 'unique_id', 'HealthCare')

class ClinitianViewset(viewsets.ModelViewSet):
	"""ClinitianViewset for REST Endpoint"""
	serializer_class = ClinitianSerializer
	permission_classes = (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			return Clinitian.objects.filter(user = user)
		else:
			return Clinitian.objects.none()

class ParentSerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= Parent
		fields  = ('user', 'email', 'first_name', 'last_name', 'address', 'contact', 'unique_id')

class ParentViewset(viewsets.ModelViewSet):
	"""ParentViewset for REST Endpoint"""
	serializer_class = ParentSerializer
	permission_classes = (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			return Parent.objects.filter(user = user)
		else:
			return Parent.objects.none()


class BabySerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= Baby
		fields  = ('first_name', 'last_name', 'tag', 'parent', 'place_of_birth', 'weight', 'blood_group', 'gender', 'birth_date', 'special_notes', 'text_notifications',)

class BabyViewset(viewsets.ModelViewSet):
	"""BabyViewset for REST Endpoint"""
	serializer_class = BabySerializer
	permission_classes = (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			return Baby.objects.filter(user = user)
		else:
			return Baby.objects.none()



router.register(r'phc_emp', ClinitianViewset, base_name = 'clinitian-rest-details')

router.register(r'parent', ParentViewset, base_name = 'parent-rest-details')

router.register(r'phc_emp', ClinitianViewset, base_name = 'clinitian-rest-details')

router.register(r'devices', FCMDeviceViewSet)

router.register(r'authdevices', FCMDeviceAuthorizedViewSet)