from django.db.models import Q
from rest_framework import viewsets
from api.serializers import DeadlineSerializer, CaseSerializer
from cases.models import Case
from remind.models import Deadline


class DeadlineViewSet(viewsets.ModelViewSet):
    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.all()

    def get_queryset(self):
        case_number = self.request.query_params.get('case', None)

        if case_number is None:
            # No case number specified
            # Get all active cases belonging to the user sorted by soonest to expire
            return super().get_queryset().filter(
                Q(case__supervisor=self.request.user) |  # TODO Separate supervisor calls from prosecutor/staff calls
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
                Q(case__supervisor=self.request.user) |  # TODO Separate supervisor calls from prosecutor/staff calls
                Q(case__prosecutor=self.request.user) |
                Q(case__secretary=self.request.user) |
                Q(case__paralegal=self.request.user) |
                Q(case__victim_advocate=self.request.user)
            )


class CaseViewSet(viewsets.ModelViewSet):
    serializer_class = CaseSerializer
    queryset = Case.objects.all()

    def get_queryset(self):
        cases = super().get_queryset().filter(
            Q(supervisor=self.request.user) |  # TODO Separate supervisor calls from prosecutor/staff calls
            Q(prosecutor=self.request.user) |
            Q(secretary=self.request.user) |
            Q(paralegal=self.request.user) |
            Q(victim_advocate=self.request.user)
        )

        return cases.exclude(closed=True)
