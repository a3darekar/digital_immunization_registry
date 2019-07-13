from __future__ import print_function
from __future__ import absolute_import

from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime
from .models import *
from .choices import *
from .choices import Vaccine_Status
from django.utils import timezone

logger = get_task_logger(__name__)


@shared_task
def add(x=10, y=20):
	print("Adding x and y")
	return x + y


@periodic_task(run_every=(crontab(minute='*/1')), name="TEST TASK 2", ignore_result=True)
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
	babies = Baby.objects.all()
	for baby in babies:
		pending_schedule = VaccineSchedule.objects.filter(week=baby.week)
		if pending_schedule:
			for obj in pending_schedule:
				if obj.status == 'pending':
					if (obj.tentative_date - now).days + 1 <= 14:
						if (obj.tentative_date - now).days >= 0:
							body = "%s is due for vaccination on %s for following vaccines of week %s" % (
								baby.get_full_name(), obj.tentative_date.date(), baby.week)
							print(body)
						else:
							body = "%s is past the due date for vaccination on %s for following vaccines of Week %s" % (
								baby.get_full_name(), obj.tentative_date.date(), baby.week)
			try:
				baby.parent.notify(
					title="Upcoming Vaccination Alert!",
					body=body,
					baby_id=baby.pk)
			except NameError:
				print("no body")
	return "completed"