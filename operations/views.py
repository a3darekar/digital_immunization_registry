# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import json
from .models import Parent, Baby, Clinitian, Appointment, VaccineRecord
from django.views.decorators.csrf import csrf_exempt
from .choices import Vaccine_names
from .twilio_credentials import *

# Create your views here.
def index(request):
	# client = Client(account_sid, auth_token)
	# message = client.messages.create(
	# 	to="+918788957859", 
	# 	from_="+13373074483",
	# 	body="Whos da gud boi?!!")

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