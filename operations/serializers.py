from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from choices import Vaccinations, Vaccine_names, Vaccine_Status
from .models import Clinitian, Parent, Baby, VaccineSchedule, VaccineRecord, Appointment, HealthCare, Notification


class ClinicianSerializer(serializers.ModelSerializer):
	class Meta:
		model = Clinitian
		fields = ('user', 'email', 'first_name', 'last_name', 'contact', 'unique_id', 'HealthCare')


class ParentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Parent
		fields = ('id', 'user', 'email', 'first_name', 'last_name', 'address', 'contact', 'unique_id')


class BabySerializer(serializers.ModelSerializer):
	class Meta:
		model = Baby
		fields = ('id', 'first_name', 'last_name', 'tag', 'parent', 'place_of_birth', 'weight', 'blood_group', 'gender',
				  'birth_date', 'special_notes', 'text_notifications', 'week')


class ParentList(generics.ListAPIView):
	serializer_class = ParentSerializer

	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		user = self.request.user
		return Parent.objects.filter(user=user)


class VaccineScheduleSerializer(serializers.ModelSerializer):
	class Meta:
		model = VaccineSchedule
		fields = ('baby', 'vaccine', 'week', 'tentative_date', 'status')

	vaccine = serializers.SerializerMethodField()

	def get_vaccine(self, obj):
		vaccinations = dict(Vaccine_names)
		obj.vaccine = vaccinations[obj.vaccine]
		return obj.vaccine


class VaccineRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = VaccineRecord
		fields = ('id', 'appointment', 'vaccine', 'status')
		read_only_fields = ('id', 'appointment', 'vaccine', 'status')


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email', 'username')

	# vaccine = serializers.SerializerMethodField()

	# def get_vaccine(self, obj):
	# 	vaccinations = dict(Vaccine_names)
	# 	obj.vaccine = vaccinations[obj.vaccine]
	# 	return obj.vaccine


class HealthCareSerializer(serializers.ModelSerializer):
	"""docstring for HealthCareSerializer"""

	class Meta:
		model = HealthCare
		fields = ('id', 'name', 'address', 'email', 'contact')
		read_only_fields = ('id', 'name', 'address', 'email', 'contact')


class AppointmentSerializer(serializers.ModelSerializer):
	administered_at = HealthCareSerializer(read_only=True)

	class Meta:
		model = Appointment
		fields = ('id', 'baby', 'administered_at', 'administered_on')
		read_only_fields = ('id', 'administered_at', 'administered_on')


class NotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notification
		fields = ('id', 'receiver', 'title', 'body', 'status', 'notif_time', 'notif_type')
