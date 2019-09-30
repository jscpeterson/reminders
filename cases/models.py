from django.db import models
from localflavor.us.models import USSocialSecurityNumberField

from reminders.models import TimeStampedModel
from users.models import CustomUser


class Judge(TimeStampedModel):
    # TODO Add courts

    last_name = models.CharField(max_length=60, )
    first_name = models.CharField(max_length=60, )
    middle_name = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)


class Case(TimeStampedModel):
    TRACK_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3')
    )

    defendant = models.CharField(max_length=120)
    case_number = models.CharField(max_length=20, unique=True)  # This is the DA Case Number
    cr_number = models.CharField(max_length=20, unique=True)
    judge = models.ForeignKey(Judge, on_delete=models.PROTECT, null=True, blank=True)
    defense_attorney = models.CharField(max_length=120, null=True, blank=True)
    notes = models.TextField(default='')

    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='supervisor')
    prosecutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='prosecutor')
    secretary = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='secretary',
                                  blank=True, null=True)
    victim_advocate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='victim_advocate',
                                  blank=True, null=True)
    paralegal = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='paralegal',
                                  blank=True, null=True)

    track = models.IntegerField(choices=TRACK_CHOICES, null=True)
    arraignment_date = models.DateTimeField(null=True)
    scheduling_conference_date = models.DateTimeField(null=True)
    pti_request_date = models.DateTimeField(null=True)
    trial_date = models.DateTimeField(null=True)

    stayed = models.BooleanField(default=False)

    closed = models.BooleanField(default=False)

    def __str__(self):
        return '{num}: {defendant}'.format(num=self.case_number, defendant=self.defendant)


class Motion(models.Model):
    INLIM = 0
    RCOR = 1
    SUPWIT = 2
    SUPEVD = 3
    SUPWITEVD = 4
    DISMISS = 5
    SUPDIS = 6
    EXTDDL = 7
    RECON = 8
    OTHER = 9

    TYPE_CHOICES = (
        (INLIM, 'In Limine'),
        (RCOR, 'Review Conditions of Release'),
        (SUPWIT, 'Motion to Suppress Witness'),
        (SUPEVD, 'Motion to Suppress Evidence'),
        (SUPWITEVD, 'Motion to Suppress Witness and Evidence'),
        (DISMISS, 'Motion to Dismiss'),
        (SUPDIS, 'Motion to Suppress and Dismiss'),
        (EXTDDL, 'Motion to Extend Deadline'),
        (RECON, 'Motion to Reconsider'),
        (OTHER, 'Other')
    )

    title = models.CharField(max_length=255,)
    type = models.IntegerField(choices=TYPE_CHOICES)
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    date_received = models.DateTimeField()
    response_deadline = models.DateTimeField(null=True, blank=True)
    date_hearing = models.DateTimeField(null=True, blank=True)
    response_filed = models.DateTimeField(null=True, blank=True)
