"""
To run rabbitmq with Docker:
    docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management

To run celery worker:
    celery -A reminders worker --loglevel=info

To run celery beat:
    celery -A reminders beat -l info
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminders.settings')

app = Celery('reminders')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@app.task
def test(arg):
    print(arg)


if __name__ == '__main__':
    app.start()
