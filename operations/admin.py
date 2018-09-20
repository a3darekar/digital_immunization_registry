from django.contrib import admin
from .models import *
from django import forms
# Register your models here.

class BabyModelForm( forms.ModelForm ):
	special_notes = forms.CharField( widget=forms.Textarea )
	class Meta:
		model = Baby
		fields = '__all__'


class ParentAdmin(admin.ModelAdmin):
	fieldsets = [
		('Login Information',		{'fields': ['user']}),
		('Account Information',		{'fields': ['first_name', 'last_name', 'unique_id']}),
		('Contact Information',		{'fields': ['address', 'contact',  'email']})
	]
	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'email', 'contact')

class ClinitianAdmin(admin.ModelAdmin):
	fieldsets = [
		('Login Information',		{'fields': ['user']}),
		('Account Information',		{'fields': ['first_name', 'last_name']}),
		('Contact Information',		{'fields': ['email', 'contact']}),
		('Misc Information',		{'fields': ['HealthCare']}),
	]
	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'email', 'contact')


class BabyAdmin(admin.ModelAdmin):
	fieldsets = [
		('Personal Information',		{'fields': ['first_name', 'last_name',]}),
		('Parent Information',			{'fields': ['parent']}),
		('Medical Information',			{'fields': ['place_of_birth', 'weight', 'blood_group', 'birth_date', 'gender']}),
		('Administration Information',	{'fields': ['tag', 'special_notes', 'text_notifications']})
	]

	form = BabyModelForm

	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'gender', 'birth_date')

class VaccineScheduleAdmin(admin.ModelAdmin):
	def Baby(self, obj):
		return obj.baby.get_full_name()

	def vaccine_status(self, obj):
		return ("%s" % (obj.status)).upper()
	vaccine_status.short_description = 'Vaccine Status'

	list_display = ('Baby', 'vaccine', 'vaccine_status', 'week', 'tentative_date')

class VaccineRecordAdmin(admin.ModelAdmin):
	"""docstring for AppointmentAdmin"""
	
	def Clinitian(self, obj):
		return obj.doctor.get_full_name()

	def Baby(self, obj):
		return obj.baby.get_full_name()

	list_display = ('Baby', 'status', 'administered_on')


admin.site.register(Parent, ParentAdmin)
admin.site.register(Baby, BabyAdmin)
admin.site.register(Clinitian, ClinitianAdmin)
admin.site.register(VaccineSchedule, VaccineScheduleAdmin)
admin.site.register(VaccineRecord, VaccineRecordAdmin)
admin.site.register(HealthCare)