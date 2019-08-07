from django.db import models
from users.models import CustomUser


class TimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        CustomUser,
        related_name='created_%(class)s_items',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    updated_by = models.ForeignKey(
        CustomUser,
        related_name='updated_%(class)s_items',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


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


class Deadline(TimeStampedModel):
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
        (WITNESS_LIST, 'Initial Witness List'),
        (REQUEST_PTI, 'PTIs Requested'),
        (CONDUCT_PTI, 'PTIs Conducted'),
        (WITNESS_PTI, 'Witness PTIs'),
        (SCIENTIFIC_EVIDENCE, 'Scientific Evidence'),
        (PRETRIAL_MOTION_FILING, 'Pretrial Motion Filing'),
        (PRETRIAL_MOTION_RESPONSE, 'Pretrial Motion Response'),
        (PRETRIAL_MOTION_HEARING, 'Pretrial Motion Hearing'),
        (PRETRIAL_CONFERENCE, 'PTC/Docket Call'),
        (FINAL_WITNESS_LIST, 'Final Witness List'),
        (NEED_FOR_INTERPRETER, 'Need for Interpreter'),
        (PLEA_AGREEMENT, 'Plea Agreement'),
        (TRIAL, 'Trial'),
    )

    ACTIVE = 0
    COMPLETED = 1
    EXPIRED = 2

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (COMPLETED, 'Complete'),
        (EXPIRED, 'Expired')
    )

    type = models.IntegerField(choices=TYPE_CHOICES)
    status = models.IntegerField(default=ACTIVE, choices=STATUS_CHOICES)
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    motion = models.ForeignKey(Motion, on_delete=models.PROTECT, null=True, blank=True)
    datetime = models.DateTimeField()
    reminders_sent = models.IntegerField(default=0)
    invalid_notice_sent = models.BooleanField(default=False)
    invalid_judge_approved = models.BooleanField(default=False)
    invalid_extension_filed = models.BooleanField(default=False)

    def first_reminder_days(self):
        return self.type

    def deadline_name(self):
        if self.type in [Deadline.PRETRIAL_MOTION_RESPONSE,]:
            label = 'Response to {motion_title}'.format(
                motion_title=self.motion.title,
            )
        elif self.type in [Deadline.PRETRIAL_MOTION_HEARING,]:
            label = 'Hearing for {motion_title}'.format(
                motion_title=self.motion.title
            )
        else:
            label = '{deadline_simple_desc}'.format(
                deadline_simple_desc=Deadline.TYPE_CHOICES[self.type][1],
            )
        return label

    def defendant(self):
        return self.case.defendant

    def case_number(self):
        return self.case.case_number

    def judge(self):
        return self.case.judge

    def defense_attorney(self):
        return self.case.defense_attorney

    def __str__(self):
        return self.TYPE_CHOICES[self.type][1]
