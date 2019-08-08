from django.db import models
from reminders.models import TimeStampedModel
from cases.models import Case, Motion


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
