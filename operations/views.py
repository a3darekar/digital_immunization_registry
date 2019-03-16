# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytz
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from .choices import Vaccine_names, BloodGroup, Vaccine_status
from .twilio_credentials import *
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .serializers import HealthCareSerializer, AppointmentSerializer, BabySerializer, VaccineScheduleSerializer, VaccineRecordSerializer, ClinitianSerializer, ParentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from fcm_django.models import FCMDevice
from django.views.generic import View
from django.db.models import Sum

# Create your views here.
def index(request):
	return HttpResponse("<h2>Error 403.</h2> You are not authorised to access this page. For further details, please contact Site Administrator.")

@csrf_exempt
def schedule_vaccines(request):
	if request.method=='POST':
		appointment 	= request.POST['appointment']
		appointment 	= Appointment.objects.get(pk=appointment)
		if appointment:
			vaccines 				= str(request.POST['vaccines'])
			vaccines 				= vaccines.split(',')
			vaccine_names			= dict(Vaccine_names)
			for vaccine in vaccines:
				vaccine_record 			= VaccineRecord(appointment = appointment, vaccine=vaccine)
				vaccine_record.save()
				baby 					= vaccine_record.appointment.baby
				vaccine_schedule 		= VaccineSchedule.objects.filter(baby=baby, vaccine=vaccine_record.vaccine)
				vaccine_schedule.status = 'scheduled'
				vaccine_schedule.save()
			return HttpResponse("{\n  appointment : " + unicode(appointment) + ", \n  list :" + unicode(vaccines) + "\n}")
		else:
			return HttpResponse("No Appointment found")
	else:
		return HttpResponse("No post data")


from .utils import render_to_pdf
from django.core.mail import EmailMessage	
from django.template.loader import get_template
from django.db.models import Count


class GeneratePdf(View):
	def get(self, request, *args, **kwargs):
		request_param =  request.GET.get("tag")
		
		if request_param:
			blood_group 		= dict(BloodGroup)
			vaccine_names		= dict(Vaccine_names)
			vaccine_status 		= dict(Vaccine_status)
			baby 				= Baby.objects.filter(tag=request_param).first()
			baby.blood_group 	= blood_group[baby.blood_group]
			schedule 			= VaccineSchedule.objects.filter(baby=baby)
			for vaccine_schedule in schedule:
				vaccine_schedule.vaccine	= vaccine_names[vaccine_schedule.vaccine]
				vaccine_schedule.status		= vaccine_status[vaccine_schedule.status]
			date = 	pytz.timezone("Asia/Kolkata").localize(datetime.today())
			context = {
				"baby": baby,
				"schedule": schedule,
				"today": date,
			}
			pdf = render_to_pdf('Scheule_report.html', context)
			filename = "Report_%s.pdf" %(context['today'])


		if request_param:
			return render(request, 'Scheule_report.html', context)
			# response = HttpResponse(html)
		 # 	return response

			# response = HttpResponse(pdf, content_type='application/pdf')
			# content = 'inline; filename="%s"' %(filename)
			# download = request.GET.get("download")
			# if download:
			# 	content = "attachment; filename='%s'" %(filename)
			# response['Content-Disposition'] = content
			# return response
		return HttpResponse("No such data found", status=201)


def notify(parent):
	email = EmailMessage('Vaccination Schedule', 'vaccination schedule of ya baby', to=[baby.parent.email], headers = {'Reply-To': 'admin@bonny.com'})
	email.attach('filename', pdf.read(), 'application/pdf')
	email.content_subtype = "html"
	email_sent = email.send()
	client 	= Client(account_sid, auth_token)
	message = client.messages.create(
		to= parent.contact, 
		from_="+13373074483",
		body="Check your MMCOE email!!")
	print message

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
				return VaccineRecord.objects.filter(appointment = appointment)
			else:
				return VaccineRecord.objects.all()
		else:
			return VaccineRecord.objects.none()

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.status = request.data.get("status")
		appointment = request.data.get("appointment")
		instance.appointment = get_object_or_404(Appointment, pk = appointment)
		baby = instance.appointment.baby
		print baby
		instance.save()
		if instance.status == 'administered':
			schedule_record = VaccineSchedule.objects.filter(baby=baby, vaccine=instance.vaccine).update(status = 'administered')
		elif instance.status == 'scheduled':
			schedule_record = VaccineSchedule.objects.filter(baby=baby, vaccine=instance.vaccine).update(status = 'scheduled')
		else:
			schedule_record = VaccineSchedule.objects.filter(baby=baby, vaccine=instance.vaccine).update(status = 'pending')
		print schedule_record
		serializer = VaccineRecordSerializer(instance=instance)
		return Response(serializer.data, status=status.HTTP_201_CREATED)



class ParentViewset(viewsets.ModelViewSet):
	"""ParentViewset for REST Endpoint"""
	serializer_class 	= ParentSerializer
	permission_classes 	= (IsAuthenticated,)

	def get_queryset(self):
		user 	= self.request.user
		pk = self.request.query_params.get('pk', None)
		if pk is not None:
			parent 	= Parent.objects.filter(user=pk)
			if user.pk == parent[0].user.pk:
				return parent
		return Parent.objects.all()

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