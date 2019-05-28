# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from datetime import datetime
from django.utils import timezone
from .models import Deadline
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def check_past_deadline(deadline):
    """ Checks to see if past deadline """
    if datetime.now() < datetime.fromisoformat(deadline):
        print('Not past deadline')
    else:
        print('Past deadline')


@shared_task
def check_all_deadlines():
    """ Checks to see if any deadlines are past due """
    now = timezone.now()
    print('Now the time is {}'.format(now.strftime('%H:%M:%S.%f')))
    for deadline in Deadline.objects.filter(expired=False):
        if deadline.datetime > now:
            print('Deadline {} NOT expired: {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))
        else:
            print('Deadline {} expired: {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))
            deadline.expired = True
            deadline.save()
            send_email(deadline)
            print('Email sent')


@shared_task()
def send_email(deadline):

    type = Deadline.TYPE_CHOICES[deadline.type][1]

    subject = 'Deadline for {type} for case {case} expired'.format(type=type, case=deadline.case.case_number)

    message = '''Hello {first_name} {last_name},
    The deadline for the {type} for case {case} expired on {date}.
 
    Thanks,
    DA 2nd Reminders
    '''.format(
        first_name=deadline.case.prosecutor_first_name,
        last_name=deadline.case.prosecutor_last_name,
        type=type,
        case=deadline.case.case_number,
        date=deadline.datetime.date(),
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            deadline.case.get_prosecutor_email(),
            deadline.case.get_supervisor_email(),
        ],
        fail_silently=True
    )


