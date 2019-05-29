# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from datetime import datetime
from django.utils import timezone

from .email import Email
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
            if deadline.type == Deadline.SCHEDULING_CONFERENCE:
                send_emails(Email.SCHEDULING_CONFERENCE, deadline)
            else:
                send_emails(Email.DEADLINE_EXPIRED, deadline)
            print('Email sent')


@shared_task()
def send_emails(email_type, deadline):

    recipients = [
        deadline.case.prosecutor,
        # deadline.case.paralegal,
        # deadline.case.supervisor,
    ]

    for recipient in recipients:
        email = Email(email_type, recipient, deadline)
        send_mail(
            subject=email.get_subject(),
            message=email.get_message(),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient.email],
            fail_silently=True
        )


