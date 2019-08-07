from __future__ import unicode_literals

import pytz
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from .choices import *
from fcm_django.models import FCMDevice

class HealthCare(models.Model):
	"""docstring for HealthCare"""
	name 		= models.CharField(max_length = 50)
	address 	= models.CharField(max_length = 140)
	email 		= models.EmailField(unique = True)
	contact 	= PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.")

	class Meta:
		verbose_name 		= ('Primary Health Care')
		verbose_name_plural = ('Primary Health Cares')

	def __str__(self):
		return self.name

class Parent(models.Model):
	"""Parent credentials for login and contact"""
	user 			= models.OneToOneField(User, help_text="Create a new user to add as a Parent or Guardian. This would be used as login credentials.")
	email 			= models.EmailField(('email address'), unique=True)
	first_name 		= models.CharField(('first name'), max_length=30, blank=True)
	last_name 		= models.CharField(('last name'), max_length=30, blank=True)
	address 		= models.CharField(max_length=200)
	contact 		= PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.")
	unique_id 		= models.CharField(('Aadhaar ID'), max_length = 13, validators=[RegexValidator(regex='^.{12}$', message='Length has to be 12', code='nomatch')])
	
	USERNAME_FIELD = 'user'
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name', contact]

	class Meta:
		verbose_name 		= ('parent')
		verbose_name_plural = ('parents')
		unique_together = (('user','id'))

	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def save(self, *args, **kwargs):
		if not self.pk:
			super(Parent, self).save()
			user = self.user
			user.first_name = self.first_name 
			user.last_name = self.last_name 
			user.email = self.email 
			user.save()
		super(Parent, self).save()

	def notify(self, title, body, text_notifications=False):
		from .twilio_credentials import  client
		device = FCMDevice.objects.all()
		if device:
			device.send_message(title, body)
		if text_notifications:
			message = client.messages.create(
				to="+918788957859",
				from_="+13373074483",
				body="%s \n %s " % (title, body)
			)
			print(message.sid)


class Clinitian(models.Model):
	"""Clinitian access"""
	user 			= models.OneToOneField(User, help_text="Create a new user to add as a  Clinitian. This would be used as login credentials.")
	email 			= models.EmailField(('email address'), unique=True)
	first_name 		= models.CharField(('first name'), max_length=30, blank=True)
	last_name 		= models.CharField(('last name'), max_length=30, blank=True)
	contact 		= PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.")
	unique_id 		= models.CharField(('Aadhaar ID'), max_length = 13, validators=[RegexValidator(regex='^.{12}$', message='Length has to be 12', code='nomatch')])
	HealthCare 		= models.ForeignKey(HealthCare)

	USERNAME_FIELD = 'user'
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name', contact]

	def __str__(self):
		return self.get_full_name()

	def save(self, *args, **kwargs):
		if not self.pk:
			super(Clinitian, self).save()
			user = self.user
			user.first_name = self.first_name 
			user.last_name = self.last_name 
			user.email = self.email 
			user.save()
		super(Clinitian, self).save()


	class Meta:
		verbose_name 		= ('Clinitian')
		verbose_name_plural = ('Clinitians')

	def get_full_name(self):

		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()
	
	def get_short_name(self):
		return self.first_name


class Baby(models.Model):
	"""Basic Details of baby"""
	first_name 			= models.CharField(('first name'), max_length=30)
	last_name 			= models.CharField(('last name'), max_length=30)
	tag 				= models.CharField(max_length = 20, unique = True)
	parent 				= models.ForeignKey(Parent, related_name = "baby")
	place_of_birth		= models.CharField(('Place of Birth'), max_length=120)
	weight				= models.PositiveIntegerField(default = 10)
	blood_group			= models.CharField('Blood Group', max_length = 10, choices = BloodGroup)
	gender				= models.CharField('Gender', max_length = 10, choices = Gender)
	birth_date			= models.DateTimeField(('Birth Date'),default=datetime.now)
	week 				= models.PositiveIntegerField(default=0)
	special_notes		= models.CharField(('Special Notes'), max_length = 400, help_text = 'Any Medical conditions such as allergies are to be mentioned here', default="NA")
	text_notifications 	= models.BooleanField(default = True)

	def __str__(self):
		return self.get_full_name()

	class Meta:
		verbose_name 		= ('baby')
		verbose_name_plural = ('babies')

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()
	
	def get_short_name(self):
		return self.first_name

	def age_in_weeks(self):
		days =  datetime.today().date().weekday() - self.birth_date.weekday() 
		return days/7

	def save(self, *args, **kwargs):
		if self.pk:
			super(Baby, self).save()	
		else:
			super(Baby, self).save()
			# Add Vaccine with the tentative date
			vaccines = dict(Vaccinations)
			for week,vaccine in vaccines.items():
				my_dict = dict(vaccine)
				for name, Name in my_dict.items():
					v = VaccineSchedule(baby = self, vaccine = name, week = week, tentative_date = self.birth_date+timedelta(week*7), status = 'pending')
					v.save()
		return self

	def dosage_complete(self, *args, **kwargs):
		vs = VaccineSchedule.objects.filter(baby=self, week=self.week).exclude(status='administered').first()
		print("inside update function")
		if vs is None:
			if self.week == 24:
				self.week = 36
			if self.week == 14:
				self.week = 24
			if self.week == 10:
				self.week = 14
			if self.week == 6:
				self.week = 10
			if self.week == 0:
				self.week = 6
			super(Baby, self).save()
		return self


class VaccineSchedule(models.Model):
	"""Schedule of Vaccines in to br Administered"""
	baby 				= models.ForeignKey(Baby, related_name = "vaccine_schedules")
	vaccine 			= models.CharField('Vaccine', max_length=20, choices=Vaccinations)
	week				= models.PositiveIntegerField(default = 0)
	tentative_date 		= models.DateTimeField(default = datetime.now)	
	status		 		= models.CharField('Vaccine Status', max_length=20, choices=Vaccine_Status)

	class Meta:
		unique_together 	= (('baby','vaccine'))
		
	def get_full_name(self):
		return self.baby

	def days_from_today(self):
		return (self.tentative_date - datetime.today().replace(tzinfo=pytz.UTC)).days


class Appointment(models.Model):
	"""List of Vaccines that have been Administered"""
	baby 				= models.ForeignKey(Baby, related_name = "vaccine_records")
	status 				= models.CharField(max_length=50, choices=Appointment_status, default='scheduled')
	administered_on 	= models.DateTimeField(default = datetime.now)	
	administered_at 	= models.ForeignKey(HealthCare, related_name="phc")
	
	def __str__(self):
		return self.baby.first_name + str(self.pk)

	def get_full_name(self):
		return self.baby

	def days_from_today(self):
		return self.tentative_date - datetime.today().date()


Vaccine_status = dict(Vaccine_Status)


class VaccineRecord(models.Model):
	"""docstring for VaccineRecord"""
	appointment = models.ForeignKey(Appointment, related_name="Appointment")
	vaccine 	= models.CharField(('Vaccine'), max_length=20, choices=Vaccinations)
	status		= models.CharField('Vaccine Status', max_length=20, choices=vaccine_record_status, default='scheduled')

	class Meta:
		unique_together 	= ("appointment", "vaccine")

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		super(VaccineRecord, self).save()
		if self.status == 'administered':
			vaccine_schedule = VaccineSchedule.objects.filter(baby=self.appointment.baby, vaccine=self.vaccine).first()
			if vaccine_schedule.status == 'scheduled':
				vaccine_schedule.status = 'administered'
				vaccine_schedule.save()
				vaccine_records = VaccineRecord.objects.filter(appointment=self.appointment, status='scheduled')
				if not vaccine_records.exists():
					self.appointment.status='completed'
					self.appointment.save()
		elif self.status == 'scheduled':
			vaccine_schedule = VaccineSchedule.objects.filter(baby=self.appointment.baby, vaccine=self.vaccine).first()
			if vaccine_schedule.status == 'pending':
				vaccine_schedule.status='scheduled'
				vaccine_schedule.save()
		else:
			vaccine_schedule = VaccineSchedule.objects.filter(baby=self.appointment.baby, vaccine=self.vaccine).first()
			if vaccine_schedule.status != 'administered':
				vaccine_schedule.status='pending'
				vaccine_schedule.save()
				vaccine_records = VaccineRecord.objects.filter(appointment=self.appointment, status='scheduled')
				if not vaccine_records.exists():
					self.appointment.status = 'completed'
					self.appointment.save()
			self.appointment.baby.dosage_complete()
		return self


class Notification(models.Model):
	"""
	Description: FCM notification Model
	"""
	receiver 	= models.ForeignKey(Parent, related_name='Parent')
	baby 		= models.ForeignKey(Baby, related_name='Baby')
	title 	 	= models.CharField(max_length=100)
	body 	 	= models.CharField(max_length=300)
	status   	= models.BooleanField(('Status'), default=False)
	notif_type 	= models.CharField(('Notification Type'), max_length=40, choices=NotificationType)
	notif_time 	= models.DateTimeField(('Notification Time'), default=datetime.now)

	class Meta:
		verbose_name = 'Notification'
		verbose_name_plural = 'Notifications'

	def save(self, *args, **kwargs):
		if self.pk:
			super(Notification, self).save()
		else:
			parent = self.receiver
			# parent.notify(self.title, self.body, self.baby.text_notifications)
			super(Notification, self).save()
