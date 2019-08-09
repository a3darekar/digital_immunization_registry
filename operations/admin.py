from django.contrib import admin
from .models import *
from django import forms


# Register your models here.


class BabyModelForm(forms.ModelForm):
	special_notes = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Baby
		fields = '__all__'


class ParentAdmin(admin.ModelAdmin):
	fieldsets = [
		('Login Information', {'fields': ['user']}),
		('Account Information', {'fields': ['first_name', 'last_name', 'unique_id']}),
		('Contact Information', {'fields': ['address', 'contact', 'email']})
	]

	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'email', 'contact')


class ClinitianAdmin(admin.ModelAdmin):
	fieldsets = [
		('Login Information', {'fields': ['user']}),
		('Account Information', {'fields': ['first_name', 'last_name']}),
		('Contact Information', {'fields': ['email', 'contact']}),
		('Misc Information', {'fields': ['HealthCare']}),
	]

	list_filter = ('HealthCare', )

	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'email', 'contact')


class BabyAdmin(admin.ModelAdmin):
	fieldsets = [
		('Personal Information', {'fields': ['first_name', 'last_name', ]}),
		('Parent Information', {'fields': ['parent']}),
		('Medical Information', {'fields': ['place_of_birth', 'weight', 'blood_group', 'birth_date', 'gender']}),
		('Administration Information', {'fields': ['tag', 'special_notes', 'text_notifications']})
	]

	list_filter = ('parent', 'week', 'blood_group', 'gender')

	form = BabyModelForm

	def name(self, obj):
		return obj.get_full_name()

	list_display = ('name', 'gender', 'birth_date', 'week')


class VaccineScheduleAdmin(admin.ModelAdmin):
	def Baby(self, obj):
		return obj.baby.get_full_name()

	def vaccine_status(self, obj):
		return ("%s" % obj.status).upper()

	vaccine_status.short_description = 'Vaccine Status'

	list_display = ('baby', 'vaccine', 'vaccine_status', 'week', 'tentative_date')

	list_filter = ('baby', 'vaccine', 'status', 'week')


class AppointmentAdmin(admin.ModelAdmin):
	"""docstring for AppointmentAdmin"""

	def Baby(self, obj):
		return obj.baby.get_full_name()

	list_display = ('id', 'baby', 'administered_at', 'status', 'administered_on')

	list_filter = ('baby', 'administered_at', 'administered_on', 'status')


class VaccineRecordAdmin(admin.ModelAdmin):
	"""docstring for VaccineRecordAdmin"""

	def Appointment(self, obj):
		return obj.appointment.pk

	list_display = ('Appointment', 'vaccine', 'status')

	list_filter = ('appointment', 'vaccine', 'status')


class NotificationAdmin(admin.ModelAdmin):
	"""docstring for VaccineRecordAdmin"""

	list_display = ('receiver', 'status', 'notif_type', 'notif_time', 'title')

	list_filter = ('receiver', 'status', 'notif_type')


admin.site.register(Parent, ParentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Baby, BabyAdmin)
admin.site.register(Clinitian, ClinitianAdmin)
admin.site.register(VaccineSchedule, VaccineScheduleAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(VaccineRecord, VaccineRecordAdmin)
admin.site.register(HealthCare)
