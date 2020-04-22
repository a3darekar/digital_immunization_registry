from django_seed import Seed
from faker import Faker
from operations.models import *
import random

fake = Faker()
seeder = Seed.seeder()

seeder.add_entity(User, 10)

seeder.add_entity(Parent, 40)

seeder.add_entity(Baby, 100, {'week': 0, 'status':'ongoing', 'birth_date': fake.date_between(start_date='-1y', end_date='today')})


insertedpks = seeder.execute()

babies = Baby.objects.all()
list = [0, 6, 10, 14, 24, 36, 40]
for baby in babies:
	choice = random.choice(list)
	birth_date = baby.birth_date
	baby.vaccine_schedules.filter(week__lt=choice).update(status='administered')
	baby.dosage_complete()
	if baby.week < 36:
		baby.status = 'dropped_out'
		baby.save()
	baby.refresh_from_db()
	vs = VaccineSchedule.objects.filter(baby=baby, status='pending', week=baby.week)
	phcs = HealthCare.objects.all()
	new_list = list[:list.index(choice)]
	for week in new_list:
		phc = random.choice(phcs)
		appointment = Appointment(baby=baby, administered_at=phc, administered_on=birth_date + timedelta(days=7*week))
		appointment.save()
		appointment.refresh_from_db()
		for v in vs:
			vr = VaccineRecord(appointment=appointment, vaccine=v.vaccine, status='administered').save()
