from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from .choices import *


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
	special_notes		= models.CharField(('Special Notes'), max_length = 400, help_text = 'Any Medical conditions such as allergies are to be mentioned here')
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
			parent = self.parent

		# Add Vaccine with the probable Dosage date
			Vaccines = dict(Vaccinations)
			for week,vaccine in Vaccines.items():
				my_dict = dict(vaccine)
				for name, Name in my_dict.items():
					v = VaccineSchedule(baby = self, vaccine = name, week = week, tentative_date = self.birth_date+timedelta(week*7), status = 'pending')
					v.save()
		return self

class VaccineSchedule(models.Model):
	"""Schedule of Vaccines in to br Administered"""
	baby 				= models.ForeignKey(Baby, related_name = "vaccine_schedules")
	vaccine 			= models.CharField('Vaccine', max_length=20, choices=Vaccinations)
	week				= models.PositiveIntegerField(default = 0)
	tentative_date 		= models.DateField(default = datetime.now)	
	status		 		= models.CharField('Vaccine Status', max_length=20, choices=Vaccine_status)
	
	def get_full_name(self):
		return self.baby

	def days_from_today(self):
		return self.tentative_date - datetime.today().date()


class VaccineRecord(models.Model):
	"""List of Vaccines that have been Administered"""
	baby 				= models.ForeignKey(Baby, related_name = "vaccine_records")
	vaccine 			= models.CharField('Vaccine', max_length=20, choices=Vaccinations)
	administered_on 	= models.DateField(default = datetime.now)	
	administered_at 	= models.DateField(default = datetime.now)	
	status		 		= models.CharField('Vaccine Status', max_length=20, choices=Vaccine_status)

		
	def get_full_name(self):
		return self.baby

	def days_from_today(self):
		return self.tentative_date - datetime.today().date()
