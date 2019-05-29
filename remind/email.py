from .models import Case, Deadline

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


class Email:

    def __init__(self, case, deadline, email_type):
        self.case = case
        self.deadline = deadline
        self.deadline_type = Deadline.TYPE_CHOICES[deadline.type][1]
        self.email_type = email_type

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
            DEADLINE_EXPIRED: 'Deadline for {type} has expired.'.format(
                type=self.deadline_type
            ),
            DEADLINE_OUTSIDE_LIMITS: 'A deadline is invalid.',
            DEADLINE_NEEDS_EXTENSION: 'A deadline requires an extension.',
            REMINDER: 'Deadline for {type} is on {datetime}.'.format(
                type=self.deadline_type,
                datetime=self.deadline.datetime
            ),
            SCHEDULING_CONFERENCE: 'Please enter scheduling information.',
            REQUEST_PTI: 'The defense may no longer request PTIs.',
            CONDUCT_PTI: 'The defense may no longer conduct PTIs.',
        }

        output += self.email_type[subjects]

        return output
