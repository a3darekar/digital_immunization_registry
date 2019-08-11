# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytz
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View
from django.db.models import Sum, Q
from rest_framework.decorators import api_view
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .twilio_credentials import *
from .choices import Vaccine_names, BloodGroup, Vaccine_Status
from .serializers import HealthCareSerializer, AppointmentSerializer, BabySerializer, VaccineScheduleSerializer, \
	VaccineRecordSerializer, ClinicianSerializer, ParentSerializer, NotificationSerializer, UserSerializer
from fcm_django.models import FCMDevice
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from rest_framework import generics
# PDF generation and Email backend imports

from .utils import render_to_pdf
from django.core.mail import EmailMessage

from django import forms


class PdfForm(forms.Form):
	tag = forms.CharField(help_text="enter tag")
	download = forms.BooleanField(initial=False, required=False)

	error_css_class = 'error'
	required_css_class = 'required'


def generatePdf(request, *args, **kwargs):
	success = ''
	if request.method == 'POST':
		form = PdfForm(request.POST)
		if form.is_valid():
			form_data = form.cleaned_data
			tag = form_data['tag']
			download = form_data['download']
			baby = get_object_or_404(Baby, tag=tag)
			blood_group = dict(BloodGroup)
			vaccine_names = dict(Vaccine_names)
			vaccine_status = dict(Vaccine_status)

			baby.blood_group = blood_group[baby.blood_group]
			schedule = VaccineSchedule.objects.filter(baby=baby)
			for vaccine_schedule in schedule:
				vaccine_schedule.vaccine = vaccine_names[vaccine_schedule.vaccine]
				vaccine_schedule.status = vaccine_status[vaccine_schedule.status]
			date = pytz.timezone("Asia/Kolkata").localize(datetime.today())
			context = {
				"baby": baby,
				"schedule": schedule,
				"today": date,
			}
			if download:
				pdf = render_to_pdf('Schedule_report.html', context)
				filename = "Immunization_Schedule_-_%s_%s" % (baby.first_name, baby.last_name)
				response = HttpResponse(pdf, content_type='application/pdf')
				content = "attachment; filename=%s.pdf" % filename
				response['Content-Disposition'] = content
				return response
			else:
				return render(request, 'Schedule_report.html', context)

	form = PdfForm()
	context = {'form': form, 'message': success}
	return render(request, 'pdf_form.html', context)


def index(request):
	return render(request, 'landing.html')


@api_view(['POST'])
def schedule_vaccines(request):
	if request.method == 'POST':
		appointment = request.POST['appointment']
		appointment = Appointment.objects.get(pk=appointment)
		if appointment:
			vaccines = str(request.POST['vaccines'])
			vaccines = vaccines.split(',')
			vaccine_names = dict(Vaccine_names)
			for vaccine in vaccines:
				vaccine_record = VaccineRecord(appointment=appointment, vaccine=vaccine)
				vaccine_record.save()
				baby = vaccine_record.appointment.baby
				schedule_record = VaccineSchedule.objects.filter(baby=baby, vaccine=vaccine).update(status='scheduled')
			return HttpResponse(
				"{\n  appointment : " + unicode(appointment) + ", \n  list :" + unicode(vaccines) + "\n}")
		else:
			return HttpResponse("No Appointment found")
	else:
		return HttpResponse("No post data")


# VIEWSETS

class UserListView(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class HealthCareViewSet(viewsets.ModelViewSet):
	"""docstring for HealthCareViewSet"""
	serializer_class = HealthCareSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		pk = self.request.query_params.get('pk', None)
		if pk is not None:
			return HealthCare.objects.filter(pk=pk)
		else:
			return HealthCare.objects.all()


class BabyViewset(viewsets.ModelViewSet):
	"""BabyViewset for REST Endpoint"""
	serializer_class = BabySerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		parent = Parent.objects.filter(user=user)
		if parent:
			return Baby.objects.filter(parent=parent)
		queryset = Baby.objects.all()
		search_param = self.request.query_params.get('search', None)
		if search_param is not None:
			parent = Parent.objects.filter(Q(contact__contains=search_param) | Q(unique_id__contains=search_param) | Q(
				email__contains=search_param))
			queryset = Baby.objects.filter(Q(tag__contains=search_param) | Q(first_name__contains=search_param) | Q(
				last_name__contains=search_param) | Q(parent=parent))
		return queryset

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.first_name = request.data.get("first_name")
		instance.last_name = request.data.get("last_name")
		instance.tag = request.data.get("tag")
		instance.place_of_birth = request.data.get("place_of_birth")
		instance.blood_group = request.data.get("blood_group")
		instance.gender = request.data.get("gender")
		instance.weight = request.data.get("weight")
		instance.week = request.data.get("week")
		instance.special_notes = request.data.get("special_notes")
		instance.text_notifications = request.data.get("text_notifications")
		instance.save()
		serializer = VaccineRecordSerializer(instance=instance)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class VaccineScheduleViewset(viewsets.ModelViewSet):
	"""VaccineScheduleViewset for REST Endpoint"""
	serializer_class = VaccineScheduleSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				baby = get_object_or_404(Baby, pk=pk)
				return VaccineSchedule.objects.filter(baby=baby)
			else:
				VaccineSchedule.objects.none()
		else:
			return Parent.objects.none()


class VaccineRecordViewset(viewsets.ModelViewSet):
	"""VaccineRecordViewset for REST Endpoint"""
	serializer_class = VaccineRecordSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				appointment = get_object_or_404(Appointment, pk=pk)
				return VaccineRecord.objects.filter(appointment=appointment)
			else:
				return VaccineRecord.objects.all()
		else:
			return VaccineRecord.objects.none()

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.status = request.data.get("status")
		appointment = request.data.get("appointment")
		instance.appointment = get_object_or_404(Appointment, pk=appointment)
		baby = instance.appointment.baby
		instance.save()
		serializer = VaccineRecordSerializer(instance=instance)
		baby.dosage_complete()
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class ParentViewset(viewsets.ModelViewSet):
	"""ParentViewset for REST Endpoint"""
	serializer_class = ParentSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		pk = self.request.query_params.get('pk', None)
		if pk is not None:
			parent = Parent.objects.filter(user=pk)
			if user.pk == parent[0].user.pk:
				return parent
		return Parent.objects.all()


class AppointmentViewSet(viewsets.ModelViewSet):
	"""docstring for AppointmentViewSet"""
	serializer_class = AppointmentSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				baby = get_object_or_404(Baby, pk=pk)
				if baby is not None:
					return Appointment.objects.filter(baby=baby)
				else:
					return VaccineRecord.objects.none()
			else:
				return VaccineRecord.objects.none()
		else:
			return VaccineRecord.objects.none()

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=False):
			user = self.request.user
			if user.is_authenticated:
				baby = serializer.validated_data['baby']
				scheduled_appointment = Appointment.objects.filter(baby=baby, status='scheduled')
				recent_appointments = Appointment.objects.filter(
					Q(baby=baby, status='completed') | Q(baby=baby, status='partial')).order_by('-administered_on')
				recent_flag = False
				days_till_vaccination = 0
				pending_vaccines = VaccineSchedule.objects.filter(baby=baby, week=baby.week)
				if not pending_vaccines:
					for recent_appointment in recent_appointments:
						if recent_appointment.days_from_today() < 28:
							recent_flag = True
							days_till_vaccination = 28 - recent_appointment.days_from_today()
							break
				if scheduled_appointment.exists():
					print(scheduled_appointment)
					return Response('Appointment Already Pending', status=status.HTTP_303_SEE_OTHER)
				elif recent_flag:
					print(recent_flag, days_till_vaccination)
					return Response('vaccination cool down period, days till vaccination: %d' % days_till_vaccination,
									status=status.HTTP_307_TEMPORARY_REDIRECT)
				else:
					print(serializer)
					self.perform_create(serializer)
					print(serializer.data)
					return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response('Failure', status=status.HTTP_403_FORBIDDEN)
		else:
			return Response('Failure', status=status.HTTP_403_FORBIDDEN)

	def perform_create(self, serializer):
		user = self.request.user
		if user.is_authenticated:
			baby = serializer.validated_data['baby']
			clinician = get_object_or_404(Clinitian, user=user)
			serializer.save(administered_at=clinician.HealthCare)


class ClinitianViewset(viewsets.ModelViewSet):
	"""ClinitianViewset for REST Endpoint"""
	serializer_class = ClinicianSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			return Clinitian.objects.filter(user=user)
		else:
			return Clinitian.objects.none()


class NotificationViewset(viewsets.ModelViewSet):
	"""NotificationViewset for REST Endpoint"""
	serializer_class = NotificationSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		user = self.request.user
		if user.is_authenticated:
			parent = Parent.objects.filter(user=user)
			return Notification.objects.filter(receiver=parent)
		else:
			return Notification.objects.none()

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		print(type(request.data.get("status")))
		if request.data.get("status") == 'true':
			instance.status = True
			instance.save()
		serializer = NotificationSerializer(instance=instance)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


router = DefaultRouter()

router.register(r'phc_emp', ClinitianViewset, base_name='clinician-rest-details')

router.register(r'healthcare', HealthCareViewSet, base_name='healthcare-list')

router.register(r'parent', ParentViewset, base_name='parent-rest')

router.register(r'babies', BabyViewset, base_name='babies-search-list')

router.register(r'vaccinations', VaccineRecordViewset, base_name='vaccine-record-list')

router.register(r'appointments', AppointmentViewSet, base_name='appointment-list')

router.register(r'schedule', VaccineScheduleViewset, base_name='vaccine-schedule-list')

router.register(r'notifications', NotificationViewset, base_name='notification-list')

router.register(r'devices', FCMDeviceViewSet)

router.register(r'authdevices', FCMDeviceAuthorizedViewSet)
