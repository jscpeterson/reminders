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

TRIAL_DEADLINES = {
    str(Deadline.WITNESS_PTI): 'Deadline to complete witness pretrial interviews',
    str(Deadline.SCIENTIFIC_EVIDENCE): 'Deadline to produce the results of scientific evidence',
    str(Deadline.PRETRIAL_MOTION_FILING): 'Deadline to file any pretrial motions',
    str(Deadline.PRETRIAL_CONFERENCE): 'Date and time of the pretrial conference',
    str(Deadline.FINAL_WITNESS_LIST): 'Deadline to submit a final witness list',
    str(Deadline.NEED_FOR_INTERPRETER): 'Deadline to file notice for language access services',
    str(Deadline.PLEA_AGREEMENT): 'Deadline to submit any plea agreement to the Court',
}
#
# DEADLINE_DESCRIPTIONS = {
#     FFA = 0
# SCHEDULING_CONFERENCE = 1
# WITNESS_LIST = 2
# REQUEST_PTI = 3
# CONDUCT_PTI = 4
# WITNESS_PTI = 5
# SCIENTIFIC_EVIDENCE = 6
# PRETRIAL_MOTION_FILING = 7
# PRETRIAL_MOTION_RESPONSE = 8
# PRETRIAL_MOTION_HEARING = 9
# PRETRIAL_CONFERENCE = 10
# FINAL_WITNESS_LIST = 11
# NEED_FOR_INTERPRETER = 12
# PLEA_AGREEMENT = 13
# TRIAL = 14
# }
