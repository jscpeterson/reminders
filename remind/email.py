from remind import utils
from .models import Deadline
from .constants import SOURCE_URL, DEADLINE_DESCRIPTIONS, SUPPORT_EMAIL

INDENT = '     '


class Email:

    DEADLINE_EXPIRED = 0
    DEADLINE_OUTSIDE_LIMITS = 1
    DEADLINE_NEEDS_EXTENSION = 2
    FIRST_REMINDER = 3
    SECOND_REMINDER = 4
    SCHEDULING_CONFERENCE = 5
    REQUEST_PTI = 6
    CONDUCT_PTI = 7

    EMAIL_TYPES = (
        (DEADLINE_EXPIRED, 'Deadline expired'),
        (DEADLINE_OUTSIDE_LIMITS, 'Deadline outside limits'),
        (DEADLINE_NEEDS_EXTENSION, 'Deadline needs extension to be valid'),
        (FIRST_REMINDER, 'First reminder'),
        (SECOND_REMINDER, 'Second reminder'),
        (SCHEDULING_CONFERENCE, 'Day of scheduling conference'),
        (REQUEST_PTI, 'Day defense can no longer request PTI'),
        (CONDUCT_PTI, 'Day defense can no longer conduct PTI')
    )

    def __init__(self, email_type, recipient, deadline):
        self.email_type = email_type
        self.recipient = recipient
        self.deadline = deadline
        self.deadline_desc = DEADLINE_DESCRIPTIONS[str(deadline.type)]
        self.case = deadline.case

    '''
    SAMPLE_DICT = {
        DEADLINE_EXPIRED: '',
        DEADLINE_OUTSIDE_LIMITS: '',
        DEADLINE_NEEDS_EXTENSION: '',
        REMINDER: '',
        SCHEDULING_CONFERENCE: '',
        REQUEST_PTI: '',
        CONDUCT_PTI: '',
    }
    '''

    def get_subject(self):
        output = 'Case {}: '.format(self.case.case_number)

        subjects = {
            self.DEADLINE_EXPIRED: '{desc} has expired.'.format(
                desc=self.deadline_desc.capitalize()
            ),
            self.DEADLINE_OUTSIDE_LIMITS: 'A deadline is invalid.',
            self.DEADLINE_NEEDS_EXTENSION: 'A deadline requires an extension.',
            self.FIRST_REMINDER: '{desc} is on {date}.'.format(
                desc=self.deadline_desc.capitalize(),
                date=self.deadline.datetime.date()
            ),
            self.SECOND_REMINDER: 'Second reminder - {desc} is on {date}.'.format(
                desc=self.deadline_desc.capitalize(),
                date=self.deadline.datetime.date()
            ),
            self.SCHEDULING_CONFERENCE: 'Please enter scheduling information.',
            self.REQUEST_PTI: 'PTIs sanctions availability',
            self.CONDUCT_PTI: 'Reminder - 30 days from date of PTI request.',
        }

        output += subjects[self.email_type]

        return output

    def get_message(self):
        header = 'Dear {first_name} {last_name}:\n\n'.format(
            first_name=self.recipient.first_name,
            last_name=self.recipient.last_name,
        )

        messages = {
            self.DEADLINE_EXPIRED: self.get_deadline_expired_message(),
            self.DEADLINE_OUTSIDE_LIMITS: self.get_deadline_invalid_message(),
            self.DEADLINE_NEEDS_EXTENSION: self.get_deadline_extension_message(),
            self.FIRST_REMINDER: self.get_first_reminder_message(),
            self.SECOND_REMINDER: self.get_second_reminder_message(),
            self.SCHEDULING_CONFERENCE: self.get_scheduling_message(),
            self.REQUEST_PTI: self.get_request_pti_message(),
            self.CONDUCT_PTI: self.get_conduct_pti_message(),
        }
        body = messages[self.email_type]

        footer = '\n\nDA 2nd Reminders'

        return header + body + footer

    def get_deadline_expired_message(self):
        return '''{indent}The {desc} for case {case} expired on {date}. Administration has been notified.'''.format(
            indent=INDENT,
            desc=self.deadline_desc,
            case=self.case.case_number,
            date=self.deadline.datetime.date(),
        )

    def get_deadline_invalid_message(self):
        url = '{source}/remind/judge_confirmed/{pk}'.format(
            source=SOURCE_URL,
            pk=self.deadline.pk,
        )

        update_url = '{source}/remind/update/{case_number}'.format(
            source=SOURCE_URL,
            case_number=self.deadline.case.case_number,
        )

        required_days = utils.get_deadline_dict(self.deadline.case.track)[str(self.deadline.type)]

        if self.deadline.type == Deadline.PRETRIAL_MOTION_RESPONSE:
            motion_clause = ' or is over 10 days from the motion filing,'
        else:
            motion_clause = ''

        return '''{indent}The {desc} is over {days} days from the triggering event,{motion_clause} which may be in \
violation of LR2-308. Please visit {url} to confirm that the judge is aware of this, or visit {update_url} to change \
the date.'''.format(
            indent=INDENT,
            desc=self.deadline_desc,
            days=required_days,
            motion_clause=motion_clause,
            url=url,
            update_url=update_url,
        )

    def get_deadline_extension_message(self):
        url = '{source}/remind/extension/{pk}'.format(
            source=SOURCE_URL,
            pk=self.deadline.pk,
        )

        update_url = '{source}/remind/update/{case_number}'.format(
            source=SOURCE_URL,
            case_number=self.deadline.case.case_number,
        )

        # If a track has not been set yet no deadlines will need an extension
        # This variable must be set to something however to prevent an exception
        if self.deadline.case.track is None:
            required_days = 0
        else:
            required_days = utils.get_deadline_dict(self.deadline.case.track)[str(self.deadline.type)]

        return '''{indent}The {desc} is over {days} days from the triggering event, which is permissible if an \
extension has been filed. Please visit {url} to confirm that you have filed for an extension, or visit {update_url} to \
change the date.'''.format(
            indent=INDENT,
            desc=self.deadline_desc,
            days=required_days,
            url=url,
            update_url=update_url,
        )

    def get_first_reminder_message(self):
        if self.deadline.type == Deadline.PRETRIAL_MOTION_RESPONSE:
            url = '{source}/remind/motion_response/{pk}'.format(
                source=SOURCE_URL,
                pk=self.deadline.motion.pk
            )
        else:
            url = '{source}/remind/complete/{pk}'.format(
                source=SOURCE_URL,
                pk=self.deadline.pk,
            )

        return '''{indent}This is a reminder that the {desc} for case {case} is on {date}. If this task has \
been completed or is not necessary in this case, please go to {url} to notify the office. If you encounter any \
problems, please notify {contact}.'''.format(
            indent=INDENT,
            desc=self.deadline_desc,
            case=self.case.case_number,
            date=self.deadline.datetime.date(),
            url=url,
            contact=SUPPORT_EMAIL,
        )

    def get_second_reminder_message(self):
        return self.get_first_reminder_message() + '''\n\n{indent}{supervisor} has received a copy of this message. \
Administration will be notified if the task is not completed by {date}.'''.format(
            indent=INDENT,
            supervisor=self.case.supervisor,
            date=self.deadline.datetime.date(),
            contact=SUPPORT_EMAIL,
        )

    def get_scheduling_message(self):
        url = '{source}/remind/track/{case_number}'.format(
            source=SOURCE_URL,
            case_number=self.case.case_number
        )

        # Need to define these values even if there is no scheduling conference date to prevent runtime error
        if self.case.scheduling_conference_date is not None:
            date = self.case.scheduling_conference_date.date()
            time = self.case.scheduling_conference_date.strftime('%H:%M')
        else:
            date = ''
            time = ''

        return '''{indent}The scheduling conference for case {case_number} was due to take place on {date}. \
Please enter the results of the scheduling order at {url}.'''.format(
            indent=INDENT,
            case_number=self.case.case_number,
            date=date,
            url=url,
        )

    def get_request_pti_message(self):
        url = '{source}/remind/request_pti/{case_number}'.format(
            source=SOURCE_URL,
            case_number=self.case.case_number
        )
        try:
            request_pti_days = utils.get_deadline_dict(self.case.track)[str(Deadline.REQUEST_PTI)]
        except KeyError:  # Thrown when there is no case track (should not happen, but default necessary for this class)
            request_pti_days = 14

        return '''{indent}It has been {days} days since the scheduling conference for case {case_number}. If the \
defense requested pretrial interviews, please enter the date they did so at {url}. If they did not timely request PTIs,\
 then under LR2-308(F)(5)(a)(vii), LR2-308(F)(5)(b)(vii), and LR2-308(F)(5)(c)(vii), "the court shall not consider \
failure to conduct pretrial interviews of witnesses as the basis of any sanction."'''.format(
            indent=INDENT,
            days=request_pti_days,
            case_number=self.case.case_number,
            url=url
        )

    def get_conduct_pti_message(self):
        try:
            conduct_pti_days = utils.get_deadline_dict(self.case.track)[str(Deadline.CONDUCT_PTI)]
        except KeyError:  # Thrown when there is no case track (should not happen, but default necessary for this class)
            conduct_pti_days = 14

        return '''{indent}It has been {days} days since the defense requested pretrial interviews for case \
{case_number}. If PTIs have been set up and conducted, you can disregard this message. If not, then please get them \
scheduled as soon as possible.'''.format(
            indent=INDENT,
            days=conduct_pti_days,
            case_number=self.case.case_number,
        )
