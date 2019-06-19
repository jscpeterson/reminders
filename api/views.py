from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets

from api.serializers import DeadlineSerializer, CaseSerializer
from remind.models import Deadline, Case


class DeadlineViewSet(viewsets.ModelViewSet):
    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
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
