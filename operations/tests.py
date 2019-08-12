# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from random import randint
from django.test import TestCase
from django_seed import Seed
from .models import *
from .serializers import *


# Create your tests here.
class TestAppointmentStatuses(TestCase):
	def setUp(self):
		seeder = Seed.seeder()
		seeder.add_entity(User, 50)
		seeder.add_entity(Parent, 1)
		seeder.add_entity(Baby, 6, {'week': 0})
		seeder.add_entity(HealthCare, 1)
		insertedpks = seeder.execute()

		babies = Baby.objects.all()
		list = [0, 6, 10, 14, 24, 36]
		for baby in babies:
			choice = random.choice(list)
			baby.vaccine_schedules.filter(week__lt=choice).update(status='administered')
			baby.dosage_complete()
			baby.refresh_from_db()
			print(baby.week)
			vs = VaccineSchedule.objects.filter(baby=baby, status='pending', week=baby.week)
			print(vs)
			phc = HealthCare.objects.first()
			appointment = Appointment(baby=baby, administered_at=phc)
			appointment.save()
			appointment.refresh_from_db()
			print(appointment.status)
			for v in vs:
				print(v.vaccine, v.status)
				vr = VaccineRecord(appointment=appointment, vaccine=v.vaccine)
				vr.save()


	def dose_completed(self):
		queryset = Baby.objects.all()
		for baby in queryset:
			pending_count = VaccineSchedule.objects.filter(baby=baby, status='pending', week__lt=baby.week).count()
			assert pending_count == 0

	def schedule_appointment(self):
		queryset = Baby.objects.all()
		for baby in queryset:
			vs = VaccineSchedule.objects.filter(baby=baby, status='pending', week=baby.week).first()
			vaccine = vs.vaccine
			phc=HealthCare.objects.first()
			appointment = Appointment(baby=baby, administered_at=phc)
			appointment.save()
			vr = VaccineRecord(appointment=appointment, vaccine=vaccine)
			vr.save()
			print(vr.appointment.baby.vaccine_schedules.filter(vaccine=vaccine).first().status)
			vs = VaccineSchedule.objects.get(pk=vs.pk)
			print(vr.status, vaccine, vs.status)
			assert vr.status == vs.status

	def check_schedule_administered(self):
		vaccineRecords = VaccineRecord.objects.all()
		for vaccineRecord in vaccineRecords:
			schedule_status = vaccineRecord.appointment.baby.vaccine_schedules.filter(vaccine=vaccineRecord.vaccine).first().status
			vaccineRecord.status = 'administered'
			vaccineRecord.save()
			schedule_status = vaccineRecord.appointment.baby.vaccine_schedules.filter(vaccine=vaccineRecord.vaccine).first().status
			assert schedule_status == 'administered'
			print(vaccineRecord.appointment.status)
			assert vaccineRecord.appointment.status == 'completed'

	def check_schedule_cancelled(self):
		vaccineRecords = VaccineRecord.objects.all()
		for vaccineRecord in vaccineRecords:
			schedule_status = vaccineRecord.appointment.baby.vaccine_schedules.filter(vaccine=vaccineRecord.vaccine).first().status
			vaccineRecord.status = 'cancelled'
			vaccineRecord.save()
			schedule = vaccineRecord.appointment.baby.vaccine_schedules.filter(vaccine=vaccineRecord.vaccine).first()
			print(vaccineRecord.status, vaccineRecord.appointment.status, schedule_status, schedule.status)
			assert schedule.status == 'pending'
			assert vaccineRecord.appointment.status == 'cancelled'

	def check_partial(self):
		appointments = Appointment.objects.all()
		for appointment in appointments:
			first_vr = VaccineRecord.objects.filter(appointment=appointment)
			counter = first_vr.count()
			first_vr = first_vr.first()
			first_vr.status = 'administered'
			first_vr.save()
			appointment.refresh_from_db()
			schedule = first_vr.appointment.baby.vaccine_schedules.filter(vaccine=first_vr.vaccine).first()
			print(first_vr.status, appointment.status, appointment, schedule.status, counter)
			assert schedule.status == 'administered'
			assert appointment.status == 'scheduled' if counter > 1 else 'completed'

	def check_scheduled_to_partial(self):
		appointments = Appointment.objects.all()
		for appointment in appointments:
			assert appointment.status == 'scheduled'
			vr = VaccineRecord.objects.filter(appointment=appointment).first()
			vr.status='administered'
			vr.save()
			print(vr)
			appointment.refresh_from_db()
			assert appointment.status == 'partial'

	def test_check_partial_to_completed(self):
		appointments = Appointment.objects.all()
		for appointment in appointments:
			assert appointment.status == 'scheduled'
			vrs = VaccineRecord.objects.filter(appointment=appointment)
			print(vrs)
			vr = vrs.first()
			if vr:
				vr.status = 'administered'
				vr.save()
				appointment.refresh_from_db()
				assert appointment.status == 'partial'
				week = appointment.baby.week
				print(week)
				for vr in vrs:
					vr.status = 'administered'
					vr.save()
					appointment.refresh_from_db()
					print(vr.status, appointment.status)
				assert appointment.status == 'completed'

	def test_check_cancel_after_partial(self):
		appointments = Appointment.objects.all()
		for appointment in appointments:
			assert appointment.status == 'scheduled'
			vrs = VaccineRecord.objects.filter(appointment=appointment)
			print(vrs)
			vr = vrs.first()
			vr.status = 'administered'
			vr.save()
			appointment.refresh_from_db()
			assert appointment.status == 'partial'
			week = appointment.baby.week
			print(week)
			for vr in vrs:
				vr.status = 'cancelled'
				vr.save()
				appointment.refresh_from_db()
				print(vr.status, appointment.status)
			assert appointment.status == 'completed'

