""" Constants used by Adult Felony processes """
from models import Deadline

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
    str(Deadline.TRIAL): 210,
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
