from .models import Case, Deadline


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
        self.deadline_type = Deadline.TYPE_CHOICES[deadline.type][1]
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
            self.DEADLINE_EXPIRED: 'Deadline for {type} has expired.'.format(
                type=self.deadline_type
            ),
            self.DEADLINE_OUTSIDE_LIMITS: 'A deadline is invalid.',
            self.DEADLINE_NEEDS_EXTENSION: 'A deadline requires an extension.',
            self.REMINDER: 'Deadline for {type} is on {datetime}.'.format(
                type=self.deadline_type,
                datetime=self.deadline.datetime
            ),
            self.SCHEDULING_CONFERENCE: 'Please enter scheduling information.',
            self.REQUEST_PTI: 'The defense may no longer request PTIs.',
            self.CONDUCT_PTI: 'The defense may no longer conduct PTIs.',
        }

        output += self.email_type[subjects]

        return output

    def get_message(self):

        header = 'Dearest user: \n'  # TODO Get real header

        messages = {
            self.DEADLINE_EXPIRED: self.get_deadline_expired_message(),
            self.DEADLINE_OUTSIDE_LIMITS: self.get_deadline_invalid_message(),
            self.DEADLINE_NEEDS_EXTENSION: self.get_deadline_extension_message(),
            self.REMINDER: self.get_reminder_message(),
            self.SCHEDULING_CONFERENCE: self.get_scheduling_message(),
            self.REQUEST_PTI: self.get_request_pti_message(),
            self.CONDUCT_PTI: self.get_conduct_pti_message(),
        }
        body = messages[self.email_type]

        footer = 'Sincerely, \nReminderBot4000'  # TODO Get real footer

        return header + body + footer

    def get_deadline_expired_message(self):
        # TODO Add message method
        raise Exception('Message not implemented')

    def get_deadline_invalid_message(self):
        # TODO Add message method
        raise Exception('Message not implemented')

    def get_deadline_extension_message(self):
        # TODO Add message method
        raise Exception('Message not implemented')

    def get_reminder_message(self):
        # TODO Add message method
        raise Exception('Message not implemented')

    def get_scheduling_message(self):
        # TODO Add message method
        raise Exception('Message not implemented')

    def get_request_pti_message(self):
        # TODO Add message method
        raise Exception('Message not implemented')

    def get_conduct_pti_message(self):
        # TODO Add message method
        raise Exception('Message not implemented')
