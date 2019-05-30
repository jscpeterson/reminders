from remind import utils
from .models import Case, Deadline
from .constants import SOURCE_URL, DEADLINE_DESCRIPTIONS

INDENT = '     '


class Email:

    DEADLINE_EXPIRED = 0
    DEADLINE_OUTSIDE_LIMITS = 1
    DEADLINE_NEEDS_EXTENSION = 2
    REMINDER = 3
    SCHEDULING_CONFERENCE = 4
    REQUEST_PTI = 5
    CONDUCT_PTI = 6

    EMAIL_TYPES = (
        (DEADLINE_EXPIRED, 'Deadline expired'),
        (DEADLINE_OUTSIDE_LIMITS, 'Deadline outside limits'),
        (DEADLINE_NEEDS_EXTENSION, 'Deadline needs extension to be valid'),
        (REMINDER, 'Reminder'),
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
            self.REMINDER: '{desc} is on {date}.'.format(
                desc=self.deadline_desc.capitalize(),
                date=self.deadline.datetime.date()
            ),
            self.SCHEDULING_CONFERENCE: 'Please enter scheduling information.',
            self.REQUEST_PTI: 'The defense may no longer request PTIs.',
            self.CONDUCT_PTI: 'The defense may no longer conduct PTIs.',
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
            # self.DEADLINE_OUTSIDE_LIMITS: self.get_deadline_invalid_message(),
            # self.DEADLINE_NEEDS_EXTENSION: self.get_deadline_extension_message(),
            # self.REMINDER: self.get_reminder_message(),
            self.SCHEDULING_CONFERENCE: self.get_scheduling_message(),
            self.REQUEST_PTI: self.get_request_pti_message(),
            self.CONDUCT_PTI: self.get_conduct_pti_message(),
        }
        body = messages[self.email_type]

        footer = '\n\nSincerely, \nReminderBot4000'

        return header + body + footer

    def get_deadline_expired_message(self):
        return '''{indent}The {desc} for case {case} expired on {date}.'''.format(
            indent=INDENT,
            desc=self.deadline_desc,
            case=self.case.case_number,
            date=self.deadline.datetime.date(),
        )

    # def get_deadline_invalid_message(self):
    #     # TODO Add message method
    #     raise Exception('Message not implemented')
    #
    # def get_deadline_extension_message(self):
    #     # TODO Add message method
    #     raise Exception('Message not implemented')
    #
    # def get_reminder_message(self):
    #     # TODO Add message method
    #     raise Exception('Message not implemented')

    def get_scheduling_message(self):
        url = '{source}/remind/{case_number}/track'.format(
            source=SOURCE_URL,
            case_number=self.case.case_number
        )

        return '''{indent}The scheduling conference for case {case_number} was due to take place on {date} at {time}. \
Please enter the results of the scheduling order at {url}.'''.format(
            indent=INDENT,
            case_number=self.case.case_number,
            date=self.case.scheduling_conference_date.date(),
            time=self.case.scheduling_conference_date.time(),  # TODO Format properly
            url=url,
        )

    def get_request_pti_message(self):
        url = '{source}/remind/{case_number}/request_pti'.format(
            source=SOURCE_URL,
            case_number=self.case.case_number
        )
        try:
            request_pti_days = utils.get_deadline_dict(self.case.track)[str(Deadline.REQUEST_PTI)]
        except utils.InvalidCaseTrackException:
            request_pti_days = 14

        return '''{indent}It has been {days} days since the scheduling conference for case {case_number}. If the \
defense requested pretrial interviews, please enter the date they did so at {url}. If they did not, you are under no \
longer under any obligation to assist them.'''.format(
            indent=INDENT,
            days=request_pti_days,
            case_number=self.case.case_number,
            url=url
        )

    def get_conduct_pti_message(self):
        try:
            conduct_pti_days = utils.get_deadline_dict(self.case.track)[str(Deadline.CONDUCT_PTI)]
        except utils.InvalidCaseTrackException:
            conduct_pti_days = 14

        return '''{indent}It has been {days} days since the defense requested pretrial interviews for case \
{case_number} on {date}. If the defense has set up and conducted their pretrial interviews, you can disregard this \
message. If they did not, this is a notification that you are no longer under any obligation to assist them.'''.format(
            indent=INDENT,
            date=self.case.pti_request_date,
            days=conduct_pti_days,
            case_number=self.case.case_number,
        )
