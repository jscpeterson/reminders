from material.forms import ModelForm, Form
from .models import Case, Deadline
from django import forms
from datetime import datetime
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
        super(SchedulingForm, self).__init__()

        case = Case.objects.get(case_number=kwargs['case_num'])

        self.fields['scheduling_date'] = forms.DateTimeField(
            label='Date of the Scheduling Conference',
            input_formats=['%Y-%m-%d']
        )

        initial = utils.get_actual_deadline_from_start(case.arraignment_date, SCHEDULING_ORDER_DEADLINE_DAYS)

        self.fields['scheduling_deadline'] = forms.DateTimeField(
            label='Maximum Possible Date',
            initial=initial,
            widget=forms.DateInput(),  # TODO Figure out how to remove time
            input_formats=['']
        )


class TrackForm(Form):
    pass


class TrialForm(Form):
    pass


class OrderForm(Form):
    pass
