from .models import Case, Deadline
from django.db.models import Q


def get_cases(user):
    cases = Case.objects.filter(
        Q(prosecutor=user) |
        Q(secretary=user) |
        Q(supervisor=user)
    )
    return cases


def get_open(cases):
    return Deadline.objects.filter(case__in=cases, status=Deadline.ACTIVE).order_by('datetime')


def get_closed(cases):
    return cases.exclude(deadline__status=Deadline.ACTIVE)
