from django.shortcuts import render
from rest_framework import viewsets

from api.serializers import DeadlineSerializer, CaseSerializer
from remind.models import Deadline, Case


class DeadlineViewSet(viewsets.ModelViewSet):
    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.all()


class CaseViewSet(viewsets.ModelViewSet):
    serializer_class = CaseSerializer
    queryset = Case.objects.all()
