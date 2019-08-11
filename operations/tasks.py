from __future__ import absolute_import
from __future__ import print_function

from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.utils import timezone

from .models import *


@periodic_task(run_every=(crontab(ignore_result=True)), name="TEST")
def add(x, y):
    return x + y


@periodic_task(run_every=(crontab(day_of_week='sunday', hour=5, minute=0)), name="NOTIFIER TASK", ignore_result=True)
def update_schedule():
	###
	# 1. retrieve objects
	# 2. get data schedule
	# 3. check current time and schedule
	# 4. create notification message if estimated date is less than 2 weeks
	# 5. send notifications via text or FCM
	###
	now = timezone.now() + timedelta(weeks=4) + timedelta(days=2)
	# statuses = Vaccine_Status
	# print(statuses)
	from .choices import Vaccine_names
	names = dict(Vaccine_names)
	babies = Baby.objects.all()

	for baby in babies:
		flag1 = flag2 = False
		upcoming = []
		overdue = []
		pending_schedule = VaccineSchedule.objects.filter(week=baby.week)
		if pending_schedule:
			for obj in pending_schedule:
				if obj.status == 'pending':
					if obj.days_from_today() + 1 <= 14:
						if obj.days_from_today() >= 0:
							flag1 = True
							upcoming.append(obj.vaccine)
						else:
							overdue.append(obj.vaccine)
							flag2 = True
			if flag2 is True:
				overdue_string = ', '.join(str(names[e]) for e in overdue)
				body = "%s is past the due date for vaccination on %s for following vaccines of Week %s for following vaccines: %s." % (
					baby.get_full_name(), obj.tentative_date.date(), baby.week, overdue_string)
				Notification(title="Overdue Vaccination Alert!", body=body, receiver=baby.parent, notif_type='danger', baby=baby).save()

			elif flag1 is True:
				upcoming_string = ', '.join(str(names[e]) for e in upcoming)
				body = "%s is due for vaccination on %s for following vaccines of week %s  for following vaccines: %s." % (
					baby.get_full_name(), obj.tentative_date.date(), baby.week, upcoming_string)
				Notification(title="Upcoming Vaccination Alert!", body=body, receiver=baby.parent, notif_type='info', baby=baby).save()

		else:
			return "incomplete"
	return "completed"
