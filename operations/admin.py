# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin

# Register your models here.
class HealthCareAdmin(admin.ModelAdmin):
	fieldsets = [
		('Basic Information',		{'fields': ['name', 'email']}),
		('Contact Information',		{'fields': ['address', 'contact']})
	]
	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'email', 'address', 'contact')	


class ParentAdmin(admin.ModelAdmin):
	fieldsets = [
		('Login Information',		{'fields': ['user']}),
		('Account Information',		{'fields': ['first_name', 'last_name', 'email', 'unique_id']}),
		('Contact Information',		{'fields': ['address', 'contact']})
	]
	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'email', 'contact')	


class ClinitianAdmin(admin.ModelAdmin):
	fieldsets = [
		('Login Information',				{'fields': ['user']}),
		('Account Information',				{'fields': ['first_name', 'last_name', 'unique_id']}),
		('Contact Information',				{'fields': ['email', 'contact']}),
		('Health Care Centre Information',	{'fields': ['health_care_centre']}),
	]
	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'email', 'contact')	


class BabyAdmin(admin.ModelAdmin):
	fieldsets = [
		('Parent Information',			{'fields': ['parent']}),
		('Personal Information',		{'fields': ['first_name', 'last_name', 'tag']}),
		('Medical Information',			{'fields': ['special_notes']}),
		('Miscellaneous Information',	{'fields': ['place_of_birth', 'blood_group', 'weight', 'gender', 'birth_date', 'text_notifications']})
	]
	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'gender', 'birth_date')


class VaccineScheduleAdmin(admin.ModelAdmin):
	def Baby(self, obj):
		return obj.baby.get_full_name()

	def vaccine_status(self, obj):
		return ("%s" % (obj.status)).upper()
	vaccine_status.short_description = 'Vaccine Status'

	list_display = ('Baby', 'vaccine', 'vaccine_status', 'week', 'tentative_vaccination_date')


admin.site.register(HealthCare, HealthCareAdmin)

admin.site.register(Parent, ParentAdmin)

admin.site.register(Clinitian, ClinitianAdmin)

admin.site.register(Baby, BabyAdmin)

admin.site.register(VaccineSchedule, VaccineScheduleAdmin)

admin.site.register(VaccineRecord)
