from django.db import models
from localflavor.us.models import USSocialSecurityNumberField

from reminders.models import TimeStampedModel
from users.models import CustomUser


class Defendant(TimeStampedModel):
    MALE = 1
    FEMALE = 2
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3

    TIER_CHOICES = (
        (TIER_1, 'Tier 1'),
        (TIER_2, 'Tier 2'),
        (TIER_3, 'Tier 3'),
    )

    mdc_num = models.IntegerField(null=True, blank=True)
    last_name = models.CharField(max_length=60, )
    first_name = models.CharField(max_length=60, )
    middle_name = models.CharField(max_length=60, null=True, blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES, null=True, blank=True)
    birth_date = models.DateField()

    ssn = USSocialSecurityNumberField(unique=True)
    fbi_number = models.CharField(max_length=9, null=True, blank=True)
    state_id = models.CharField(max_length=8, null=True, blank=True)

    # phone_number = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    tier = models.IntegerField(choices=TIER_CHOICES, null=True, blank=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    @property
    def name(self):
        return str(self)


class DefenseAttorney(TimeStampedModel):
    last_name = models.CharField(max_length=60, )
    first_name = models.CharField(max_length=60, )
    middle_name = models.CharField(max_length=60, null=True, blank=True)
    firm = models.CharField(max_length=180, null=True, blank=True)

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)


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

    defendant = models.ForeignKey(Defendant, on_delete=models.PROTECT, blank=True, null=True)
    case_number = models.CharField(max_length=20, unique=True)  # This is the DA Case Number
    cr_number = models.CharField(max_length=20, unique=True)
    judge = models.ForeignKey(Judge, on_delete=models.PROTECT, null=True, blank=True)
    defense_attorney = models.CharField(max_length=120, null=True, blank=True)
    notes = models.TextField(default='')

    prosecutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='prosecutor')
    secretary = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='secretary')
    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='supervisor')

    track = models.IntegerField(choices=TRACK_CHOICES, null=True)
    arraignment_date = models.DateTimeField(null=True)
    scheduling_conference_date = models.DateTimeField(null=True)
    pti_request_date = models.DateTimeField(null=True)
    trial_date = models.DateTimeField(null=True)

    stayed = models.BooleanField(default=False)

    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.case_number


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
