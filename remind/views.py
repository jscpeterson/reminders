# from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Case
from .forms import CaseForm


class CaseCreate(CreateView):
    model = Case
    form_class = CaseForm
    success_url = '/remind/create/'
