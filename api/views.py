from django.db.models import Q
from rest_framework import viewsets
from api.serializers import DeadlineSerializer, CaseSerializer
from remind.models import Deadline, Case


class DeadlineViewSet(viewsets.ModelViewSet):
    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.all()

    def get_queryset(self):
        case_number = self.request.query_params.get('case', None)

        if case_number is None:
            return super().get_queryset().filter(
                Q(case__supervisor=self.request.user) |
                Q(case__prosecutor=self.request.user) |
                Q(case__secretary=self.request.user)
            )
        elif not Case.objects.filter(case_number=case_number).exists():
            return []
        else:
            case_pk = Case.objects.get(case_number=case_number).pk
            return super().get_queryset().filter(case=case_pk).filter(
                Q(case__supervisor=self.request.user) |
                Q(case__prosecutor=self.request.user) |
                Q(case__secretary=self.request.user)
            )


class CaseViewSet(viewsets.ModelViewSet):
    serializer_class = CaseSerializer
    queryset = Case.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(supervisor=self.request.user) |
            Q(prosecutor=self.request.user) |
            Q(secretary=self.request.user)
        )
