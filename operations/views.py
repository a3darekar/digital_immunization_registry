# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from .choices import Vaccine_names
from .twilio_credentials import *
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from .serializers import HealthCareSerializer, AppointmentSerializer, BabySerializer, VaccineScheduleSerializer, VaccineRecordSerializer, ClinitianSerializer, ParentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from fcm_django.models import FCMDevice

# Create your views here.
def index(request):
	client = Client(account_sid, auth_token)
	message = client.messages.create(
		to="+918788957859", 
		from_="+13373074483",
		body="Kuth Rahilis?!!")

	print repr(message)
	devices = FCMDevice.objects.all()
	print devices
	for device in devices:
		body = "Eee" + " Sejal :- " + "Kuth Rahilis?"
		device.send_message(title="Testing Messges", body=body)

	return HttpResponse("<h2>Error 403.</h2> You are not authorised to access this page. For further details, please contact Site Administrator.")


@csrf_exempt
def schedule_vaccines(request):
	# message = client.messages.create(
	# 	to="+918788957859", 
	# 	from_="+13373074483",
	# 	body="Hello from Python! Have a nice day!")

	# print(message.sid)
	if request.method=='POST':
		appointment = request.POST['appointment']
		appointment = Appointment.objects.get(pk=appointment)
		if appointment:
			vaccines = str(request.POST['vaccines'])
			vaccines = vaccines.split(',')
			print vaccines
			vaccine_names	= dict(Vaccine_names)
			for vaccine in vaccines:
				vaccinerecord = VaccineRecord(appointment = appointment, vaccine=vaccine)
				print vaccine_names[vaccine]
				vaccinerecord.save()
			return HttpResponse("{\n  appointment : " + unicode(appointment) + ", \n  list :" + unicode(vaccines) + "\n}")
		else:
			return HttpResponse("No Appointment found")
	else:
		return HttpResponse("No post data")


#VIEWSETS


class HealthCareViewSet(viewsets.ModelViewSet):
	"""docstring for HealthCareViewSet"""
	serializer_class 	= HealthCareSerializer
	permission_classes  = (IsAuthenticated, )

	def get_queryset(self):
		pk = self.request.query_params.get('pk', None)
		if pk is not None:
			return HealthCare.objects.filter(pk = pk)
		else:
			return HealthCare.objects.all()


class BabyViewset(viewsets.ModelViewSet):
	"""BabyViewset for REST Endpoint"""
	serializer_class 	= BabySerializer
	permission_classes 	= (IsAuthenticated,)

	def get_queryset(self):
		user 		= self.request.user
		parent 		= Parent.objects.filter(user = user)
		if parent:
			return Baby.objects.filter(parent = parent)
		queryset 	= Baby.objects.all()
		tag 		= self.request.query_params.get('tag', None)
		email 		= self.request.query_params.get('email', None)
		contact		= self.request.query_params.get('contact', None)
		name 		= self.request.query_params.get('name', None)
		aadhaar 	= self.request.query_params.get('aadhaar', None)
		if tag is not None:
			queryset = Baby.objects.filter(tag__contains = tag)
		elif name is not None:
			queryset = Baby.objects.filter(first_name__contains = name) | Baby.objects.filter(last_name__contains = name) 
		elif email is not None:
			parent = Parent.objects.filter(email = email)
			queryset = Baby.objects.filter(parent = parent)
		elif contact is not None:
			parent = Parent.objects.filter(contact = contact)
			queryset = Baby.objects.filter(parent = parent)
		elif aadhaar is not None:
			parent = Parent.objects.filter(unique_id = aadhaar)
			print parent
			queryset = Baby.objects.filter(parent = parent)
		return queryset



class VaccineScheduleViewset(viewsets.ModelViewSet):
	"""VaccineScheduleViewset for REST Endpoint"""
	serializer_class 	= VaccineScheduleSerializer
	permission_classes 	= (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				baby = get_object_or_404(Baby, pk = pk)
				return VaccineSchedule.objects.filter(baby = baby)
			else:
				VaccineSchedule.objects.none()
		else:
			return Parent.objects.none()



class VaccineRecordViewset(viewsets.ModelViewSet):
	"""VaccineRecordViewset for REST Endpoint"""
	serializer_class 	= VaccineRecordSerializer
	permission_classes 	= (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				appointment = get_object_or_404(Appointment, pk = pk)
				if appointment is not None:
					return VaccineRecord.objects.filter(appointment = appointment)
				else:
					return VaccineRecord.objects.none()
			else:
				return VaccineRecord.objects.none()
		else:
			return VaccineRecord.objects.none()



class ParentViewset(viewsets.ModelViewSet):
	"""ParentViewset for REST Endpoint"""
	serializer_class 	= ParentSerializer
	permission_classes 	= (IsAuthenticated,)
	queryset 			= Parent.objects.all()


class AppointmentViewSet(viewsets.ModelViewSet):
	"""docstring for AppointmentViewSet"""
	serializer_class 	= AppointmentSerializer
	permission_classes 	= (IsAuthenticated, )

	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				baby = get_object_or_404(Baby, pk = pk)
				if baby is not None:
					return Appointment.objects.filter(baby = baby)
				else:
					return VaccineRecord.objects.none()
			else:
				return VaccineRecord.objects.none()
		else:
			return VaccineRecord.objects.none()

	def perform_create(self, serializer):
		user = self.request.user
		if user.is_authenticated:
			clinitian = get_object_or_404(Clinitian, user = user)
			healthcare = clinitian.HealthCare
			serializer.save(administered_at=healthcare)



class ClinitianViewset(viewsets.ModelViewSet):
	"""ClinitianViewset for REST Endpoint"""
	serializer_class 	= ClinitianSerializer
	permission_classes 	= (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			return Clinitian.objects.filter(user = user)
		else:
			return Clinitian.objects.none()




router = DefaultRouter()

router.register(r'phc_emp', ClinitianViewset, base_name = 'clinitian-rest-details')

router.register(r'healthcare', HealthCareViewSet, base_name = 'healthcare-list')

router.register(r'parent', ParentViewset, base_name = 'parent-rest')

router.register(r'babies',BabyViewset, base_name = 'babies-search-list')

router.register(r'vaccinations',VaccineRecordViewset, base_name = 'vaccine-record-list')

router.register(r'appointments',AppointmentViewSet, base_name = 'appointment-list')

router.register(r'schedule',VaccineScheduleViewset, base_name = 'vaccine-schedule-list')

router.register(r'devices', FCMDeviceViewSet)

router.register(r'authdevices', FCMDeviceAuthorizedViewSet)