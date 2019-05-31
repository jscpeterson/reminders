""" Constants used by Adult Felony processes """
from .models import Deadline

SOURCE_URL = 'http://127.0.0.1:8000'

SCHEDULING_ORDER_DEADLINE_DAYS = 30

LAST_DAY_HOUR = 23
LAST_DAY_MINUTE = 59
LAST_DAY_SECOND = 59
MIN_DAYS_FOR_DEADLINES = 11
SATURDAY = 5
SUNDAY = 6

TRACK_ONE_DEADLINE_LIMITS = {
    str(Deadline.TRIAL): 210,
    'trial_extended': 240,
    str(Deadline.WITNESS_LIST): 25,  # Days after arraignment
    str(Deadline.REQUEST_PTI): 14,  # Days after scheduling order
    str(Deadline.CONDUCT_PTI): 30,  # Days after PTI request
    str(Deadline.WITNESS_PTI): 60,  # Days before trial
    str(Deadline.SCIENTIFIC_EVIDENCE): 120,  # Days before trial
    'scientific_evidence_extended': 90,  # Days before trial
    str(Deadline.PRETRIAL_MOTION_FILING): 50,  # Days before trial
    str(Deadline.PRETRIAL_MOTION_RESPONSE): 40,  # Days before trial OR 10 days after filing
    str(Deadline.PRETRIAL_MOTION_HEARING): 35,  # Days before trial
    str(Deadline.PRETRIAL_CONFERENCE): 15,  # Days before trial
    str(Deadline.FINAL_WITNESS_LIST): 15,  # Days before trial
    str(Deadline.NEED_FOR_INTERPRETER): 15,  # Days before trial
    str(Deadline.PLEA_AGREEMENT): 10,  # Days before trial
}

TRACK_TWO_DEADLINE_LIMITS = {
    str(Deadline.TRIAL): 300,
    'trial_extended': 360,
    str(Deadline.WITNESS_LIST): 25,  # Days after arraignment
    str(Deadline.REQUEST_PTI): 21,  # Days after scheduling order
    str(Deadline.CONDUCT_PTI): 45,  # Days after PTI request
    str(Deadline.WITNESS_PTI): 75,  # Days before trial
    str(Deadline.SCIENTIFIC_EVIDENCE): 120,  # Days before trial
    'scientific_evidence_extended': 90,  # Days before trial
    str(Deadline.PRETRIAL_MOTION_FILING): 60,  # Days before trial
    str(Deadline.PRETRIAL_MOTION_RESPONSE): 45,  # Days before trial OR 10 days after filing
    str(Deadline.PRETRIAL_MOTION_HEARING): 35,  # Days before trial
    str(Deadline.PRETRIAL_CONFERENCE): 15,  # Days before trial
    str(Deadline.FINAL_WITNESS_LIST): 15,  # Days before trial
    str(Deadline.NEED_FOR_INTERPRETER): 15,  # Days before trial
    str(Deadline.PLEA_AGREEMENT): 10,  # Days before trial
}

TRACK_THREE_DEADLINE_LIMITS = {
    str(Deadline.TRIAL): 455,
    'trial_extended': 545,
    str(Deadline.WITNESS_LIST): 25,  # Days after arraignment
    str(Deadline.REQUEST_PTI): 21,  # Days after scheduling order
    str(Deadline.CONDUCT_PTI): 60,  # Days after PTI request
    str(Deadline.WITNESS_PTI): 100,  # Days before trial
    str(Deadline.SCIENTIFIC_EVIDENCE): 150,  # Days before trial
    'scientific_evidence_extended': 120,  # Days before trial
    str(Deadline.PRETRIAL_MOTION_FILING): 70,  # Days before trial
    str(Deadline.PRETRIAL_MOTION_RESPONSE): 55,  # Days before trial OR 10 days after filing
    str(Deadline.PRETRIAL_MOTION_HEARING): 45,  # Days before trial
    str(Deadline.PRETRIAL_CONFERENCE): 20,  # Days before trial
    str(Deadline.FINAL_WITNESS_LIST): 20,  # Days before trial
    str(Deadline.NEED_FOR_INTERPRETER): 15,  # Days before trial
    str(Deadline.PLEA_AGREEMENT): 10,  # Days before trial
}

TRIAL_DEADLINES = [
    str(Deadline.WITNESS_PTI),
    str(Deadline.SCIENTIFIC_EVIDENCE),
    str(Deadline.PRETRIAL_MOTION_FILING),
    str(Deadline.PRETRIAL_CONFERENCE),
    str(Deadline.FINAL_WITNESS_LIST),
    str(Deadline.NEED_FOR_INTERPRETER),
    str(Deadline.PLEA_AGREEMENT),
]

DEADLINE_DESCRIPTIONS = {
    # str(Deadline.FFA): '',
    str(Deadline.SCHEDULING_CONFERENCE): 'date of the scheduling conference',
    str(Deadline.WITNESS_LIST): 'deadline to file a witness list',
    str(Deadline.REQUEST_PTI): 'deadline for the defense to request pretrial interviews',
    str(Deadline.CONDUCT_PTI): 'deadline for the defense to conduct pretrial interviews',
    str(Deadline.WITNESS_PTI): 'deadline to complete witness pretrial interviews',
    str(Deadline.SCIENTIFIC_EVIDENCE): 'deadline to produce the results of scientific evidence',
    str(Deadline.PRETRIAL_MOTION_FILING): 'deadline to file any pretrial motions',
    # str(Deadline.PRETRIAL_MOTION_RESPONSE): '',
    # str(Deadline.PRETRIAL_MOTION_HEARING): '',
    str(Deadline.PRETRIAL_CONFERENCE): 'date and time of the pretrial conference',
    str(Deadline.FINAL_WITNESS_LIST): 'deadline to submit a final witness list',
    str(Deadline.NEED_FOR_INTERPRETER): 'deadline to file notice for language access services',
    str(Deadline.PLEA_AGREEMENT): 'deadline to submit any plea agreement to the Court',
    str(Deadline.TRIAL): 'date the trial will commence',
}

FIRST_REMINDER_DAYS = {
    # str(Deadline.FFA): '',
    str(Deadline.SCHEDULING_CONFERENCE): 5,
    str(Deadline.WITNESS_LIST): 5,
    str(Deadline.REQUEST_PTI): 5,
    str(Deadline.CONDUCT_PTI): 5,
    str(Deadline.WITNESS_PTI): 5,
    str(Deadline.SCIENTIFIC_EVIDENCE): 5,
    str(Deadline.PRETRIAL_MOTION_FILING): 5,
    # str(Deadline.PRETRIAL_MOTION_RESPONSE): '',
    # str(Deadline.PRETRIAL_MOTION_HEARING): '',
    str(Deadline.PRETRIAL_CONFERENCE): 5,
    str(Deadline.FINAL_WITNESS_LIST): 5,
    str(Deadline.NEED_FOR_INTERPRETER): 5,
    str(Deadline.PLEA_AGREEMENT): 5,
    str(Deadline.TRIAL): 5,
}

SECOND_REMINDER_DAYS = {
    # str(Deadline.FFA): '',
    str(Deadline.SCHEDULING_CONFERENCE): 2,
    str(Deadline.WITNESS_LIST): 2,
    str(Deadline.REQUEST_PTI): 2,
    str(Deadline.CONDUCT_PTI): 2,
    str(Deadline.WITNESS_PTI): 2,
    str(Deadline.SCIENTIFIC_EVIDENCE): 2,
    str(Deadline.PRETRIAL_MOTION_FILING): 2,
    # str(Deadline.PRETRIAL_MOTION_RESPONSE): '',
    # str(Deadline.PRETRIAL_MOTION_HEARING): '',
    str(Deadline.PRETRIAL_CONFERENCE): 2,
    str(Deadline.FINAL_WITNESS_LIST): 2,
    str(Deadline.NEED_FOR_INTERPRETER): 2,
    str(Deadline.PLEA_AGREEMENT): 2,
    str(Deadline.TRIAL): 2,
}
