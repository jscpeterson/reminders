from material.forms import ModelForm, Form
from .models import Case
from django import forms
from . import utils
from .constants import SCHEDULING_ORDER_DEADLINE_DAYS


class CaseForm(ModelForm):
    # TODO Prevent user from being able to enter duplicate case
    class Meta:
        model = Case
        fields = ['case_number',
                  'prosecutor_first_name',
                  'prosecutor_last_name',
                  'paralegal_first_name',
                  'paralegal_last_name',
                  'supervisor_first_name',
                  'supervisor_last_name',
                  'arraignment_date']


class SchedulingForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        initial = utils.get_actual_deadline_from_start(case.arraignment_date, SCHEDULING_ORDER_DEADLINE_DAYS)
        self.fields['scheduling_conference_date'] = forms.DateTimeField(
            label='Scheduling Conference',
            initial=initial
        )


class TrackForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        self.fields['track'] = forms.ChoiceField(
            choices=Case.TRACK_CHOICES,
            label='What is the case track?',
        )


class TrialForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])


class OrderForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])
