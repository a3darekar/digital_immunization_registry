from django_seed import Seed
from faker import Faker
from operations.models import *
import random

fake = Faker()
seeder = Seed.seeder()
seeder.add_entity(User, 40)
seeder.add_entity(Parent, 40)
seeder.add_entity(Baby, 100, {'week': 0, 'status':'ongoing', 'birth_date': fake.date_between(start_date='-1y', end_date='today')})
insertedpks = seeder.execute()

babies = Baby.objects.all()
list = [0, 6, 10, 14, 24, 36, 40]
for baby in babies:
	choice = random.choice(list)
	birth_date = baby.birth_date
	phcs = HealthCare.objects.all()
	new_list = list[:list.index(choice)]
	for week in new_list:
		phc = random.choice(phcs)
		administered_on = birth_date + timedelta(days=7*week)
		appointment = Appointment(baby=baby, administered_at=phc, administered_on=administered_on)
		appointment.save()
		vs = VaccineSchedule.objects.filter(baby=baby, week=week)
		for v in vs:
			v.status='administered'
			v.save()
			vr = VaccineRecord(appointment=appointment, vaccine=v.vaccine).save()
			vr.status='administered'
			vr.save()
	if baby.week == 36:
		baby.status = 'completed'
	else:
		baby.status = 'dropped_out'
	baby.save()
	print(baby.status)
	