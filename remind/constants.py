from .models import Deadline

SOURCE_URL = 'http://127.0.0.1:8000'
ADMINISTRATION_EMAIL = 'joseph.peterson@da2nd.state.nm.us'
SUPPORT_EMAIL = 'coders@da2nd.state.nm.us'

SCHEDULING_ORDER_DEADLINE_DAYS = 30
WITNESS_LIST_DEADLINE_DAYS = 25

LAST_DAY_HOUR = 23
LAST_DAY_MINUTE = 59
LAST_DAY_SECOND = 59
MIN_DAYS_FOR_DEADLINES = 11
SATURDAY = 5
SUNDAY = 6

TRACKLESS_DEADLINE_LIMITS = {
    str(Deadline.SCHEDULING_CONFERENCE): SCHEDULING_ORDER_DEADLINE_DAYS,  # Days after arraignment
    str(Deadline.WITNESS_LIST): WITNESS_LIST_DEADLINE_DAYS,  # Days after arraignment
}

TRACK_ONE_DEADLINE_LIMITS = {
    str(Deadline.TRIAL): 210,
    'trial_extended': 240,
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
TRACK_ONE_DEADLINE_LIMITS.update(TRACKLESS_DEADLINE_LIMITS)

TRACK_TWO_DEADLINE_LIMITS = {
    str(Deadline.TRIAL): 300,
    'trial_extended': 360,
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
TRACK_TWO_DEADLINE_LIMITS.update(TRACKLESS_DEADLINE_LIMITS)

TRACK_THREE_DEADLINE_LIMITS = {
    str(Deadline.TRIAL): 455,
    'trial_extended': 545,
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
TRACK_THREE_DEADLINE_LIMITS.update(TRACKLESS_DEADLINE_LIMITS)

TRIAL_DEADLINES = (
    str(Deadline.WITNESS_PTI),
    str(Deadline.SCIENTIFIC_EVIDENCE),
    str(Deadline.PRETRIAL_MOTION_FILING),
    str(Deadline.PRETRIAL_CONFERENCE),
    str(Deadline.FINAL_WITNESS_LIST),
    str(Deadline.NEED_FOR_INTERPRETER),
    str(Deadline.PLEA_AGREEMENT),
)

# Deadlines that do not require a reminder
EVENT_DEADLINES = (
    Deadline.SCHEDULING_CONFERENCE,
    Deadline.PRETRIAL_CONFERENCE,
    Deadline.TRIAL,
    Deadline.REQUEST_PTI,
    Deadline.CONDUCT_PTI,
    Deadline.PRETRIAL_MOTION_HEARING
)

DEADLINE_DESCRIPTIONS = {
    # str(Deadline.FFA): '',
    str(Deadline.SCHEDULING_CONFERENCE): 'date of the scheduling conference',
    str(Deadline.WITNESS_LIST): 'deadline to file a witness list',
    str(Deadline.REQUEST_PTI): 'deadline for the defense to request pretrial interviews',
    str(Deadline.CONDUCT_PTI): 'deadline for the defense to conduct pretrial interviews',
    str(Deadline.WITNESS_PTI): 'deadline to complete witness pretrial interviews',
    str(Deadline.SCIENTIFIC_EVIDENCE): 'deadline to produce the results of scientific evidence',
    str(Deadline.PRETRIAL_MOTION_FILING): 'deadline to file any pretrial motions',
    str(Deadline.PRETRIAL_MOTION_RESPONSE): 'deadline to file a response to a pretrial motion',
    str(Deadline.PRETRIAL_MOTION_HEARING): 'date of a pretrial motion hearing',
    str(Deadline.PRETRIAL_CONFERENCE): 'date and time of the pretrial conference',
    str(Deadline.FINAL_WITNESS_LIST): 'deadline to submit a final witness list',
    str(Deadline.NEED_FOR_INTERPRETER): 'deadline to file notice for language access services',
    str(Deadline.PLEA_AGREEMENT): 'deadline to submit any plea agreement to the Court',
    str(Deadline.TRIAL): 'date the trial will commence',
}

FIRST_REMINDER_DAYS = {
    # Deadline.FFA): '',
    Deadline.SCHEDULING_CONFERENCE: 5,
    Deadline.WITNESS_LIST: 5,
    Deadline.REQUEST_PTI: 5,
    Deadline.CONDUCT_PTI: 5,
    Deadline.WITNESS_PTI: 5,
    Deadline.SCIENTIFIC_EVIDENCE: 5,
    Deadline.PRETRIAL_MOTION_FILING: 5,
    Deadline.PRETRIAL_MOTION_RESPONSE: 5,
    Deadline.PRETRIAL_MOTION_HEARING: 5,
    Deadline.PRETRIAL_CONFERENCE: 5,
    Deadline.FINAL_WITNESS_LIST: 5,
    Deadline.NEED_FOR_INTERPRETER: 5,
    Deadline.PLEA_AGREEMENT: 5,
    Deadline.TRIAL: 5,
}

SECOND_REMINDER_DAYS = {
    # Deadline.FFA: '',
    Deadline.SCHEDULING_CONFERENCE: 2,
    Deadline.WITNESS_LIST: 2,
    Deadline.REQUEST_PTI: 2,
    Deadline.CONDUCT_PTI: 2,
    Deadline.WITNESS_PTI: 2,
    Deadline.SCIENTIFIC_EVIDENCE: 2,
    Deadline.PRETRIAL_MOTION_FILING: 2,
    Deadline.PRETRIAL_MOTION_RESPONSE: 2,
    Deadline.PRETRIAL_MOTION_HEARING: 2,
    Deadline.PRETRIAL_CONFERENCE: 2,
    Deadline.FINAL_WITNESS_LIST: 2,
    Deadline.NEED_FOR_INTERPRETER: 2,
    Deadline.PLEA_AGREEMENT: 2,
    Deadline.TRIAL: 2,
}
