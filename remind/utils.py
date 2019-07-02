import pytz
from django.conf import settings
from datetime import timedelta
import holidays
from .models import Deadline
from .constants import SATURDAY, SUNDAY, MIN_DAYS_FOR_DEADLINES, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND, \
    TRACK_ONE_DEADLINE_LIMITS, TRACK_TWO_DEADLINE_LIMITS, TRACK_THREE_DEADLINE_LIMITS, TRACKLESS_DEADLINE_LIMITS, \
    TRIAL_DEADLINES, JUDGES, RESPONSE_AFTER_FILING_DAYS


def clear_deadlines(case):
    """ Clears all deadlines related to a case """
    for deadline in Deadline.objects.filter(case=case):
        deadline.delete()


def is_weekend_or_nm_holiday(date):
    """
    Returns True if a datetime object falls on a weekend day or a New Mexico recognized state holiday.
    :param date: a datetime object
    :return: True if a date is a weekend or a New Mexico recognized holiday
    """
    return date.weekday() in [SATURDAY, SUNDAY] or date.date() in holidays.US(state='NM', years=date.year).keys()


def count_holidays_weekends_in_range_from_start(start_date, num_days):
    return sum([1 for i in range(num_days) if is_weekend_or_nm_holiday(start_date + timedelta(days=i))])


def count_holidays_weekends_in_range_from_end(end_date, num_days):
    return sum([1 for i in range(num_days) if is_weekend_or_nm_holiday(end_date - timedelta(days=i))])


class InvalidCaseTrackException(Exception):
    pass


def get_deadline_dict(track):
    """Gets a dictionary of deadlines based on the track of a case."""
    if track is None:
        deadlines = TRACKLESS_DEADLINE_LIMITS
    elif track == 1:
        deadlines = TRACK_ONE_DEADLINE_LIMITS
    elif track == 2:
        deadlines = TRACK_TWO_DEADLINE_LIMITS
    elif track == 3:
        deadlines = TRACK_THREE_DEADLINE_LIMITS
    else:
        raise InvalidCaseTrackException('Track "{}" not valid'.format(track))
    return deadlines


def get_actual_deadline_from_start(start_date, days):
    """
    For the date of a past event and a given number of days, returns the true deadline pursuant to Statutes, Rules,
    and Const. NMRA (Unannotated) Rules of Criminal Procedure for the District Courts ARTICLE 1 General Provisions 5-104

    5-104 . Time.
    A.   Computing time.  This rule applies in computing any time period specified in these rules, in any local rule or
     court order, or in any statute, unless another Supreme Court rule of procedure contains time computation provisions
     that expressly supersede this rule.
    (1)   Period stated in days or a longer unit; eleven (11) days or more.  When the period is stated as eleven
        (11) days or a longer unit of time
            (a)   exclude the day of the event that triggers the period;
            (b)   count every day, including intermediate Saturdays, Sundays, and legal holidays; and
            (c)   include the last day of the period, but if the last day is a Saturday, Sunday, or legal holiday, the
            period continues to run until the end of the next day that is not a Saturday, Sunday, or legal holiday.

    (2)   Period stated in days or a longer unit; ten (10) days or less.  When the period is stated in days but the
        number of days is ten (10) days or less
            (a)   exclude the day of the event that triggers the period;
            (b)   exclude intermediate Saturdays, Sundays, and legal holidays; and
            (c)   include the last day of the period, but if the last day is a Saturday, Sunday, or legal holiday, the
            period continues to run until the end of the next day that is not a Saturday, Sunday, or legal holiday.

    :param start_date: the date of a past event that determines a deadline.
    :param days: the number of days from an event date until a mandatory deadline is reached.
    :return: the actual date of the deadline in accordance with 5-104
    """

    # (a) exclude the day of the event that triggers the period;
    next_day = start_date + timedelta(days=1)

    # Period stated in days or a longer unit; eleven (11) days or more.  When the period is stated as eleven (11) days
    # or a longer unit of time
    if days >= MIN_DAYS_FOR_DEADLINES:
        # (b) count every day, including intermediate Saturdays, Sundays, and legal holidays;
        result_date = next_day + timedelta(days=days)

    # Period stated in days or a longer unit; ten (10) days or less.  When the period is stated in days but the number
    # of days is ten (10) days or less
    else:
        # (b) exclude intermediate Saturdays, Sundays, and legal holidays; and
        result_date = next_day + timedelta(days=days + count_holidays_weekends_in_range_from_start(next_day, days))

    # (c) include the last day of the period,
    result_date = result_date - timedelta(days=1)

    # but if the last day is a Saturday, Sunday, or legal holiday, the
    # period continues to run until the end of the next day that is not a Saturday, Sunday, or legal holiday.
    while is_weekend_or_nm_holiday(result_date):
        result_date = result_date + timedelta(days=1)

    # Update time to (almost) midnight of next day
    # result_date = result_date.replace(tzinfo=timezone(settings.TIME_ZONE),
    #                                   hour=LAST_DAY_HOUR,
    #                                   minute=LAST_DAY_MINUTE,
    #                                   second=LAST_DAY_SECOND)

    return result_date


def get_actual_deadline_from_end(end_date, days):
    """
    For the date of a future event and a given number of days, returns the true deadline pursuant to Statutes, Rules,
    and Const. NMRA (Unannotated) Rules of Criminal Procedure for the District Courts ARTICLE 1 General Provisions 5-104

    5-104 . Time.
    A.   Computing time.  This rule applies in computing any time period specified in these rules, in any local rule or
     court order, or in any statute, unless another Supreme Court rule of procedure contains time computation provisions
     that expressly supersede this rule.
    (1)   Period stated in days or a longer unit; eleven (11) days or more.  When the period is stated as eleven
        (11) days or a longer unit of time
            (a)   exclude the day of the event that triggers the period;
            (b)   count every day, including intermediate Saturdays, Sundays, and legal holidays; and
            (c)   include the last day of the period, but if the last day is a Saturday, Sunday, or legal holiday, the
            period continues to run until the end of the next day that is not a Saturday, Sunday, or legal holiday.

    (2)   Period stated in days or a longer unit; ten (10) days or less.  When the period is stated in days but the
        number of days is ten (10) days or less
            (a)   exclude the day of the event that triggers the period;
            (b)   exclude intermediate Saturdays, Sundays, and legal holidays; and
            (c)   include the last day of the period, but if the last day is a Saturday, Sunday, or legal holiday, the
            period continues to run until the end of the next day that is not a Saturday, Sunday, or legal holiday.

    :param end_date: the date of a future event that determines a deadline.
    :param days: the number of days from an event date until a mandatory deadline is reached.
    :return: the actual date of the deadline in accordance with 5-104
    """

    # (a) exclude the day of the event that triggers the period;
    prior_day = end_date - timedelta(days=1)

    # Period stated in days or a longer unit; eleven (11) days or more.  When the period is stated as eleven (11) days
    # or a longer unit of time
    if days >= MIN_DAYS_FOR_DEADLINES:
        # (b) count every day, including intermediate Saturdays, Sundays, and legal holidays;
        result_date = prior_day - timedelta(days=days)

    # Period stated in days or a longer unit; ten (10) days or less.  When the period is stated in days but the number
    # of days is ten (10) days or less
    else:
        # (b) exclude intermediate Saturdays, Sundays, and legal holidays; and
        result_date = prior_day - timedelta(days=days + count_holidays_weekends_in_range_from_end(prior_day, days))

    # (c) include the last day of the period,
    result_date = result_date + timedelta(days=1)

    # but if the last day is a Saturday, Sunday, or legal holiday, the
    # period continues to run until the end of the next day that is not a Saturday, Sunday, or legal holiday.
    while is_weekend_or_nm_holiday(result_date):
        result_date = result_date - timedelta(days=1)

    # Update time to (almost) midnight of next day
    # result_date = result_date.replace(tzinfo=timezone(settings.TIME_ZONE),
    #                                   hour=LAST_DAY_HOUR,
    #                                   minute=LAST_DAY_MINUTE,
    #                                   second=LAST_DAY_SECOND)

    return result_date


def get_motion_response_deadline(motion):
    """
    Written responses to any pretrial motions shall be filed within ten (10) days of the filing of any pretrial
    motions and in any case not less than forty (40) days before the trial date. Failure to file a written response
    shall be deemed, for purposes of deciding the motion, an admission of the facts stated in the motion;

    Note: 40 days will vary according to case track.
    """
    deadline_dict = get_deadline_dict(motion.case.track)
    actual_deadline_from_filing = get_actual_deadline_from_start(motion.date_received, RESPONSE_AFTER_FILING_DAYS)
    actual_deadline_from_trial = get_actual_deadline_from_end(motion.case.trial_date,
                                                              deadline_dict[str(Deadline.PRETRIAL_MOTION_RESPONSE)])
    return min(actual_deadline_from_filing, actual_deadline_from_trial)


def is_deadline_within_limits(deadline, event, days, future_event=False):
    """
    Returns True if a deadline is within the acceptable limits given an event and the days required.
    :param deadline: a given deadline
    :param event: an event the deadline corresponds to
    :param days: the required number of days before or after the event
    :param future_event: an optional flag, True indicates that the event is in the future (such as a trial) and the days
    given are days required before the event takes place.
    :return: True if a deadline is acceptable, False if it is not within the limits.
    """

    if future_event:
        actual_deadline = get_actual_deadline_from_end(event, days)
        actual_deadline = actual_deadline.replace(tzinfo=pytz.timezone(settings.TIME_ZONE),
                                                  hour=LAST_DAY_HOUR, minute=LAST_DAY_MINUTE, second=LAST_DAY_SECOND)
        return actual_deadline - deadline >= timedelta(days=0)
    else:
        actual_deadline = get_actual_deadline_from_start(event, days)
        actual_deadline = actual_deadline.replace(tzinfo=pytz.timezone(settings.TIME_ZONE),
                                                  hour=LAST_DAY_HOUR, minute=LAST_DAY_MINUTE, second=LAST_DAY_SECOND)
        return actual_deadline - deadline >= timedelta(days=0)


def is_extension_required(deadline):
    """
    Returns True if a deadline requires an extension to be valid.
    :return: True if a deadline requires an extension to be valid.
    """
    # If a track has not been set yet no deadlines will need an extension
    if deadline.case.track is None:
        return False
    else:
        deadline_dict = get_deadline_dict(deadline.case.track)

    if deadline.type == Deadline.TRIAL:
        max_date_default = get_actual_deadline_from_start(deadline.case.arraignment_date,
                                                          deadline_dict[str(Deadline.TRIAL)])
        max_date_extension = get_actual_deadline_from_start(deadline.case.arraignment_date,
                                                            deadline_dict['trial_extended'])
        return max_date_default.date() < deadline.datetime.date() <= max_date_extension.date()
    elif deadline.type == Deadline.SCIENTIFIC_EVIDENCE:
        max_date_default = get_actual_deadline_from_end(deadline.case.trial_date,
                                                        deadline_dict[str(Deadline.SCIENTIFIC_EVIDENCE)])
        max_date_extension = get_actual_deadline_from_end(deadline.case.trial_date,
                                                          deadline_dict['scientific_evidence_extended'])
        return max_date_extension.date() >= deadline.datetime.date() > max_date_default.date()


class DeadlineTypeException(Exception):
    pass


def is_deadline_invalid(deadline):
    """
    Returns True if a deadline is outside permissible limits from a triggering event.
    """
    deadline_dict = get_deadline_dict(deadline.case.track)
    required_days = deadline_dict[str(deadline.type)]
    # Deadlines where the triggering event is a future trial
    if str(deadline.type) in TRIAL_DEADLINES or deadline.type == Deadline.PRETRIAL_MOTION_HEARING:
        return not is_deadline_within_limits(deadline=deadline.datetime,
                                             event=deadline.case.trial_date,
                                             days=required_days,
                                             future_event=True)

    # Deadlines where the triggering event is arraignment
    elif deadline.type in [Deadline.SCHEDULING_CONFERENCE, Deadline.WITNESS_LIST, Deadline.TRIAL]:
        return not is_deadline_within_limits(deadline=deadline.datetime,
                                             event=deadline.case.arraignment_date,
                                             days=required_days,
                                             future_event=False)

    # These are automatically generated and should not be incorrect.
    elif deadline.type in [Deadline.REQUEST_PTI]:
        return False
    elif deadline.type in [Deadline.CONDUCT_PTI]:
        return False

    # Pretrial motion responses have two considerations for their date
    if deadline.type in [Deadline.PRETRIAL_MOTION_RESPONSE]:
        return is_motion_response_deadline_invalid(deadline.motion, deadline.datetime)

    raise DeadlineTypeException('Deadline type {} not handled'.format(deadline.type))


def is_motion_response_deadline_invalid(motion, motion_response_deadline):
    """
    Written responses to any pretrial motions shall be filed within ten (10) days of the filing of any pretrial
    motions and in any case not less than forty (40) days before the trial date. Failure to file a written response
    shall be deemed, for purposes of deciding the motion, an admission of the facts stated in the motion;

    Note: 40 days will vary according to case track.
    """
    deadline_dict = get_deadline_dict(motion.case.track)
    motion_response_deadline = motion_response_deadline.replace(tzinfo=pytz.timezone(settings.TIME_ZONE),
                                                                hour=LAST_DAY_HOUR, minute=LAST_DAY_MINUTE,
                                                                second=LAST_DAY_SECOND)

    check1 = is_deadline_within_limits(
        deadline=motion_response_deadline,
        event=motion.date_received,
        days=RESPONSE_AFTER_FILING_DAYS,
        future_event=False,
    )
    check2 = is_deadline_within_limits(
        deadline=motion_response_deadline,
        event=motion.case.trial_date,
        days=deadline_dict[str(Deadline.PRETRIAL_MOTION_RESPONSE)],
        future_event=True,
    )

    return not check1 and check2


def find_judge_index(judge):
    """
    Finds the index of the judge by name in the JUDGES constant. Not an ideal way to go about this.
    """
    for judge_tuple in JUDGES:
        if judge == judge_tuple[1]:
            return judge_tuple[0] - 1


def sort_judges(case):
    """
    Returns a reorganized version of the JUDGES constant based on a case, where the first entry is the current judge
    on the case. This is a workaround to set the initial judge value in the HTML template.
    """
    judge = case.judge
    judges_list = list(JUDGES)
    judge_tuple = judges_list.pop(find_judge_index(judge))
    judges_list.insert(0, judge_tuple)
    return judges_list


def get_disabled_fields(case):
    """
    Gets the disabled fields for a case to pass into the Update Form
    """
    disabled = [False, False]  # First two fields for judge and defense attorney should not be disabled
    for deadline in Deadline.objects.filter(case=case).order_by('datetime'):
        answer = (deadline.status != Deadline.ACTIVE)
        disabled.append(answer)
        disabled.append(answer)
    return disabled
