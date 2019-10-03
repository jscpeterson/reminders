from django.db.models import Q
from rest_framework import viewsets
from api.serializers import DeadlineSerializer, CaseSerializer, UserSerializer
from cases.models import Case
from remind.models import Deadline
from users.models import CustomUser


class DeadlineViewSet(viewsets.ModelViewSet):
    """Endpoint for deadlines. Returns all active deadlines a user has a general staff position on ordered by soonest
    to expire. If a case_number param is specified, returns all deadlines on a case."""
    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.all()

    def get_queryset(self):
        case_number = self.request.query_params.get('case', None)

        if case_number is None:
            # No case number specified
            # Get all active cases belonging to the user sorted by soonest to expire
            return super().get_queryset().filter(
                Q(case__prosecutor=self.request.user) |
                Q(case__secretary=self.request.user) |
                Q(case__paralegal=self.request.user) |
                Q(case__victim_advocate=self.request.user)
            ).filter(
                status=Deadline.ACTIVE
            ).order_by(
                'datetime'
            )
        elif not Case.objects.filter(case_number=case_number).exists():
            return []
        else:
            case_pk = Case.objects.get(case_number=case_number).pk
            return super().get_queryset().filter(case=case_pk).filter(
                Q(case__prosecutor=self.request.user) |
                Q(case__secretary=self.request.user) |
                Q(case__paralegal=self.request.user) |
                Q(case__victim_advocate=self.request.user)
            )


class StaffDeadlineViewSet(viewsets.ModelViewSet):
    """Endpoint for management to view staff deadlines. Returns active deadlines for cases the user is a supervisor on,
    or if the user is a superuser, returns all active deadlines."""
    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(case__supervisor=self.request.user)

        return queryset.filter(
                    status=Deadline.ACTIVE
                ).order_by(
                    'datetime'
                )


class CaseViewSet(viewsets.ModelViewSet):
    """Endpoint for cases. Returns all cases a user has a general staff position on."""
    serializer_class = CaseSerializer
    queryset = Case.objects.all()

    def get_queryset(self):
        cases = super().get_queryset().filter(
            Q(prosecutor=self.request.user) |
            Q(secretary=self.request.user) |
            Q(paralegal=self.request.user) |
            Q(victim_advocate=self.request.user)
        )

        return cases.exclude(closed=True)


class StaffCaseViewSet(viewsets.ModelViewSet):
    """Endpoint for management to view staff cases. Returns cases the user is a supervisor on, or if the user is a
    superuser, returns all open cases."""
    serializer_class = CaseSerializer
    queryset = Case.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(supervisor=self.request.user)

        return queryset.exclude(closed=True)


class UserSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)
