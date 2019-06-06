from .models import Case, Deadline
from django.db.models import Q


def get_cases(user):
    cases = Case.objects.filter(
        Q(prosecutor=user) |
        Q(paralegal=user) |
        Q(supervisor=user)
    )
    return cases


def get_open(cases):
    return cases.filter(deadline__status=Deadline.ACTIVE)


def get_closed(cases):
    return cases.exclude(deadline__status=Deadline.ACTIVE)
