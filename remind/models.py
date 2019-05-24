from django.db import models


class Case(models.Model):
    TRACK_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3')
    )

    def get_email(self, first_name, last_name):
        return '{first}.{last}@da2nd.state.nm.us'.format(first=first_name, last=last_name)

    def get_prosecutor_email(self):
        return self.get_email(self.prosecutor_first_name, self.prosecutor_last_name)

    def get_paralegal_email(self):
        return self.get_email(self.paralegal_first_name, self.paralegal_last_name)

    def get_supervisor_email(self):
        return self.get_email(self.supervisor_first_name, self.supervisor_last_name)

    case_number = models.CharField(max_length=20)
    track = models.IntegerField(choices=TRACK_CHOICES, null=True, blank=True)

    prosecutor_first_name = models.CharField(max_length=60, null=True, blank=True)
    prosecutor_last_name = models.CharField(max_length=60, null=True, blank=True)

    paralegal_first_name = models.CharField(max_length=60, null=True, blank=True)
    paralegal_last_name = models.CharField(max_length=60, null=True, blank=True)

    supervisor_first_name = models.CharField(max_length=60, null=True, blank=True)
    supervisor_last_name = models.CharField(max_length=60, null=True, blank=True)

    arraignment_date = models.DateTimeField(null=True, blank=True)
    scheduling_conference_date = models.DateTimeField(null=True, blank=True)
    pti_request_date = models.DateTimeField(null=True, blank=True)
    trial_date = models.DateTimeField(null=True, blank=True)


class Deadline(models.Model):
    FFA = 0
    SCHEDULING_CONFERENCE = 1
    WITNESS_LIST = 2
    REQUEST_PTI = 3
    CONDUCT_PTI = 4
    WITNESS_PTI = 5
    SCIENTIFIC_EVIDENCE = 6
    PRETRIAL_MOTION_FILING = 7
    PRETRIAL_MOTION_RESPONSE = 8
    PRETRIAL_MOTION_HEARING = 9
    PRETRIAL_CONFERENCE = 10
    FINAL_WITNESS_LIST = 11
    NEED_FOR_INTERPRETER = 12
    PLEA_AGREEMENT = 13
    TRIAL = 14

    TYPE_CHOICES = (
        (FFA, 'FFA'),
        (SCHEDULING_CONFERENCE, 'Scheduling Conference'),
        (WITNESS_LIST, 'Witness List'),
        (REQUEST_PTI, 'Request PTIs'),
        (CONDUCT_PTI, 'Conduct Initial PTIs'),
        (WITNESS_PTI, 'Winess PTIs'),
        (SCIENTIFIC_EVIDENCE, 'Scientific Evidence'),
        (PRETRIAL_MOTION_FILING, 'Pretrial Motion Filing'),
        (PRETRIAL_MOTION_RESPONSE, 'Pretrial Motion Response'),
        (PRETRIAL_MOTION_HEARING, 'Pretrial Motion Hearing'),
        (PRETRIAL_CONFERENCE, 'Pretrial Conference'),
        (FINAL_WITNESS_LIST, 'Final Witness List'),
        (NEED_FOR_INTERPRETER, 'Need for Interpreter'),
        (PLEA_AGREEMENT, 'Plea Agreement'),
        (TRIAL, 'Trial'),
    )

    type = models.IntegerField(choices=TYPE_CHOICES)
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    date = models.DateTimeField()
    expired = models.BooleanField(default=False)


class Motion(models.Model):
    # type
    pass
