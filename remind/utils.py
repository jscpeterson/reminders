from datetime import timedelta
from pytz import timezone
import holidays
from reminders import settings
from .models import Deadline
from .constants import SATURDAY, SUNDAY, MIN_DAYS_FOR_DEADLINES, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND, \
    TRACK_ONE_DEADLINE_LIMITS, TRACK_TWO_DEADLINE_LIMITS, TRACK_THREE_DEADLINE_LIMITS, SCHEDULING_ORDER_DEADLINE_DAYS, \
    TRIAL_DEADLINES


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
    if track == 1:
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
    result_date = result_date.replace(tzinfo=timezone(settings.TIME_ZONE),
                                      hour=LAST_DAY_HOUR,
                                      minute=LAST_DAY_MINUTE,
                                      second=LAST_DAY_SECOND)

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
    result_date = result_date.replace(tzinfo=timezone(settings.TIME_ZONE),
                                      hour=LAST_DAY_HOUR,
                                      minute=LAST_DAY_MINUTE,
                                      second=LAST_DAY_SECOND)

    return result_date


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
        return actual_deadline - deadline >= timedelta(days=0)
    else:
        actual_deadline = get_actual_deadline_from_start(event, days)
        return deadline - actual_deadline >= timedelta(days=0)


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
        return max_date_default < deadline.datetime < max_date_extension
    elif deadline.type == Deadline.SCIENTIFIC_EVIDENCE:
        max_date_default = get_actual_deadline_from_end(deadline.case.trial_date,
                                                        deadline_dict[str(Deadline.SCIENTIFIC_EVIDENCE)])
        max_date_extension = get_actual_deadline_from_end(deadline.case.trial_date,
                                                          deadline_dict['scientific_evidence_extended'])
        return max_date_extension > deadline.datetime > max_date_default


class DeadlineTypeException(Exception):
    pass


def is_deadline_invalid(deadline):
    """
    Returns True if a deadline is outside permissible limits from a triggering event.
    """
    if deadline.type == Deadline.SCHEDULING_CONFERENCE:
        return deadline.datetime.date() > get_actual_deadline_from_start(deadline.case.arraignment_date,
                                                                         SCHEDULING_ORDER_DEADLINE_DAYS).date()
    if deadline.case.track is None:
        return False
    else:
        deadline_dict = get_deadline_dict(deadline.case.track)
        if str(deadline.type) in TRIAL_DEADLINES:
            required_days = deadline_dict[str(deadline.type)]
            date = get_actual_deadline_from_end(deadline.case.trial_date, required_days)
            return deadline.datetime.date() > date.date()

    # raise DeadlineTypeException('Deadline type {} not handled'.format(deadline.type))
