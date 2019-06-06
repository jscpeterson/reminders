from .models import Case
from django.db.models import Q


def get_cases(user):
    cases = Case.objects.filter(
        Q(prosecutor=user) |
        Q(paralegal=user) |
        Q(supervisor=user)
    )
    return cases


def get_open(cases):
    return cases.filter(deadline__expired=False).filter(deadline__completed=False)


def get_closed(cases):
    return cases.filter(Q(deadline__expired=True) | Q(deadline__completed=True))
