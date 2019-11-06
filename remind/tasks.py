# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from datetime import datetime, timedelta
from django.utils import timezone

from .models import Deadline
from .constants import FIRST_REMINDER_DAYS, SECOND_REMINDER_DAYS, ADMINISTRATION_EMAIL, EVENT_DEADLINES, \
    IMPORTANT_EVENTS, IMPORTANT_EVENT_REMINDER_DAYS, PTI_DEADLINES
from .email import Email
from . import utils
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

    emails_sent = {
        Email.DEADLINE_NEEDS_EXTENSION: 0,
        Email.DEADLINE_OUTSIDE_LIMITS: 0,
        Email.EVENT_REMINDER: 0,
        Email.SCHEDULING_CONFERENCE: 0,
        Email.REQUEST_PTI: 0,
        Email.CONDUCT_PTI: 0,
        Email.DEADLINE_EXPIRED: 0,
        Email.FIRST_REMINDER: 0,
        Email.SECOND_REMINDER: 0,
    }

    now = timezone.now()
    print('Now the time is {}'.format(now.strftime('%H:%M:%S.%f')))

    for deadline in Deadline.objects.filter(status=Deadline.ACTIVE, case__stayed=False):
        days_until = deadline.datetime - now

        # TEMPORARILY REMOVING DUE TO COMPLAINTS
        # Send notice if celery detects a deadline is invalid or requires an extension
        # if utils.is_extension_required(deadline) and not deadline.invalid_notice_sent:
        #     print('Deadline {} requires an extension.'.format(deadline.pk))
        #     send_emails(Email.DEADLINE_NEEDS_EXTENSION, deadline, emails_sent)
        #     deadline.invalid_notice_sent = True
        #     deadline.save(update_fields=['invalid_notice_sent'])
        #     continue
        # elif utils.is_deadline_invalid(deadline) and not deadline.invalid_notice_sent:
        #     print('Deadline {} requires judge approval.'.format(deadline.pk))
        #     send_emails(Email.DEADLINE_OUTSIDE_LIMITS, deadline, emails_sent)
        #     deadline.invalid_notice_sent = True
        #     deadline.save(update_fields=['invalid_notice_sent'])
        #     continue

        # If deadline is in PTI_DEADLINES handle similar to an EVENT_DEADLINE
        if deadline.type in PTI_DEADLINES:
            if days_until <= timedelta(days=0):
                if deadline.type == Deadline.REQUEST_PTI:
                    send_emails(Email.REQUEST_PTI, deadline, emails_sent)
                if deadline.type == Deadline.CONDUCT_PTI:
                    send_emails(Email.CONDUCT_PTI, deadline, emails_sent)
            continue

        # If deadline is in EVENT_DEADLINES it does not need a deadline expiry notice and uses different reminders
        if deadline.type in EVENT_DEADLINES:

            # Month long reminder for Trial.
            if deadline.type == Deadline.TRIAL \
                and days_until.days <= FIRST_REMINDER_DAYS[Deadline.TRIAL] \
                    and deadline.reminders_sent == 0:
                send_emails(Email.EVENT_REMINDER, deadline, emails_sent)
                deadline.reminders_sent += 1
                deadline.save(update_fields=['reminders_sent'])
                print('Reminder sent for event {} on {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))

            # If it is approaching the deadline and this is an important event, send a courtesy reminder.
            if deadline.type in IMPORTANT_EVENTS \
                and days_until.days <= IMPORTANT_EVENT_REMINDER_DAYS \
                    and deadline.reminders_sent == 0:
                send_emails(Email.EVENT_REMINDER, deadline, emails_sent)
                deadline.reminders_sent += 1
                deadline.save(update_fields=['reminders_sent'])
                print('Reminder sent for event {} on {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))

            # If it is past the deadline, send emails in specific cases, otherwise, silently complete the task.
            if days_until <= timedelta(days=0):
                if deadline.type == Deadline.SCHEDULING_CONFERENCE:
                    send_emails(Email.SCHEDULING_CONFERENCE, deadline, emails_sent)
                deadline.status = Deadline.COMPLETED
                deadline.save(update_fields=['status'])
                print('Deadline {} completed: {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))
                continue

        else:
            # If it is past the deadline, send expiry emails and flag the deadline as expired
            if days_until < timedelta(days=0):
                print('Deadline {} expired: {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))
                send_emails(Email.DEADLINE_EXPIRED, deadline, emails_sent)
                deadline.status = Deadline.EXPIRED
                deadline.save(update_fields=['status'])
                continue
            # Send first reminder if it is within the FIRST_REMINDER time and no reminders have been sent
            elif (days_until <= timedelta(days=FIRST_REMINDER_DAYS[deadline.type])) and deadline.reminders_sent < 1:
                print('Reminder sent for deadline {} on {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))
                send_emails(Email.FIRST_REMINDER, deadline, emails_sent)
                deadline.reminders_sent += 1
                deadline.save(update_fields=['reminders_sent'])
                continue
            # Send second reminder if it is within the SECOND_REMINDER time and two reminders have not been sent
            elif (days_until <= timedelta(days=SECOND_REMINDER_DAYS[deadline.type])) and deadline.reminders_sent < 2:
                print('Reminder sent for deadline {} on {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))
                send_emails(Email.SECOND_REMINDER, deadline, emails_sent)
                deadline.reminders_sent += 1
                deadline.save(update_fields=['reminders_sent'])
                continue

        # If code has not hit continue, deadline does not need to do anything.
        # print('Deadline {} NOT expired: {}'.format(deadline.pk, deadline.datetime.strftime('%H:%M:%S.%f')))

    send_admin_report(emails_sent)


@shared_task
def send_emails(email_type, deadline, emails_sent):

    # https://docs.djangoproject.com/en/2.2/topics/email/#sending-multiple-emails

    recipient_emails = [
        deadline.case.prosecutor.email,
    ]

    for staff_member in [deadline.case.secretary, deadline.case.paralegal, deadline.case.victim_advocate]:
        if staff_member is not None:
            recipient_emails.append(staff_member.email)

    if email_type == Email.SECOND_REMINDER:
        recipient_emails.append(deadline.case.supervisor.email)
    elif email_type == Email.DEADLINE_EXPIRED:
        recipient_emails.append(deadline.case.supervisor.email)
        recipient_emails.append(ADMINISTRATION_EMAIL)

    email = Email(email_type, deadline.case.prosecutor, deadline)
    send_mail(
        subject=email.get_subject(),
        message=email.get_message(),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_emails,
        fail_silently=True
    )

    emails_sent[email_type] += len(recipient_emails)
    print('\nCASE: {case_num} TYPE: {email_type} {deadline_type}{num_recipients} emails sent to {recipients}.'.format(
        case_num=deadline.case.case_number,
        email_type=Email.EMAIL_TYPES[email_type][1],
        deadline_type='DEADLINE: {} '.format(deadline) if email_type in Email.DEADLINE_EMAIL_TYPES else '',
        num_recipients=len(recipient_emails),
        recipients=str(recipient_emails),
    ))


@shared_task
def send_admin_report(emails_sent):
    # TODO Flesh out daily email to include git info, celery worker info.
    if not settings.DEBUG:

        message = 'This is a daily report to notify you that the \'{server_name}\' server is sending emails.'.format(
            server_name=settings.SERVER_NAME
        )
        message += '\n{num_emails} emails were sent out to users this morning.'.format(
            num_emails=sum(emails_sent.values())
        )
        message += '\n\n - ReminderBot 4000'

        send_mail(
            subject='Daily report {}'.format(datetime.now().strftime('%c')),
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.SYSADMIN_EMAIL],
            fail_silently=True, 
        )
        print('Daily report email sent.')
