from __future__ import print_function
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bonny.settings')
app = Celery('bonny')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'print_hello',
        'schedule': 30.0,
        'args': (16, 16)
    },
}


@app.task
def print_hello():
    print('hello there')
