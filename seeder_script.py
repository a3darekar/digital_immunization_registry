from django_seed import Seed
from operations.models import *
import random

seeder = Seed.seeder()

seeder.add_entity(User, 50)
seeder.add_entity(HealthCare, 2)
seeder.add_entity(Clinitian, 10)

seeder.add_entity(Parent, 40)
seeder.add_entity(Baby, 100, {'week': 0})


insertedpks = seeder.execute()

babies = Baby.objects.all()
list = [0, 6, 10, 14, 24, 36]
for baby in babies:
	choice = random.choice(list)
	baby.vaccine_schedules.filter(week__lt=choice).update(status='administered')
	baby.dosage_complete()
	baby.refresh_from_db()
	vs = VaccineSchedule.objects.filter(baby=baby, status='pending', week=baby.week)
	phcs = HealthCare.objects.all()
	phc = random.choice(phcs)
	appointment = Appointment(baby=baby, administered_at=phc)
	appointment.save()
	appointment.refresh_from_db()
	for v in vs:
		vr = VaccineRecord(appointment=appointment, vaccine=v.vaccine, status='adminsitered')
		vr.save()
