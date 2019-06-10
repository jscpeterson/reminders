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


class Case(TimeStampedModel):
    TRACK_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3')
    )

    prosecutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='prosecutor')
    paralegal = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='paralegal')
    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='supervisor')
    case_number = models.CharField(max_length=20, unique=True)
    track = models.IntegerField(choices=TRACK_CHOICES, null=True)
    arraignment_date = models.DateTimeField(null=True)
    scheduling_conference_date = models.DateTimeField(null=True)
    pti_request_date = models.DateTimeField(null=True)
    trial_date = models.DateTimeField(null=True)


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
        (WITNESS_LIST, 'Witness List'),
        (REQUEST_PTI, 'Defense Request PTIs'),
        (CONDUCT_PTI, 'Defense Conduct PTIs'),
        (WITNESS_PTI, 'Witness PTIs'),
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
    datetime = models.DateTimeField()
    reminders_sent = models.IntegerField(default=0)
    invalid_notice_sent = models.BooleanField(default=False)
    invalid_judge_approved = models.BooleanField(default=False)
    invalid_extension_filed = models.BooleanField(default=False)

    def __str__(self):
        return self.TYPE_CHOICES[self.type][1]


class Motion(models.Model):
    # type
    pass
