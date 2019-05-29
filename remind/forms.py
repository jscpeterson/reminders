from django.forms import ModelForm, Form
from .models import Case, Deadline
from users.models import CustomUser
from django import forms
from datetime import datetime
from . import utils
from .constants import SCHEDULING_ORDER_DEADLINE_DAYS


class CaseForm(ModelForm):
    supervisor = forms.ModelChoiceField(queryset=CustomUser.objects.filter(position=1), empty_label=None)
    prosecutor = forms.ModelChoiceField(queryset=CustomUser.objects.filter(position=2), empty_label=None)
    paralegal = forms.ModelChoiceField(queryset=CustomUser.objects.filter(position=3), empty_label=None)
    arraignment_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])

    class Meta:
        model = Case
        fields = ['case_number',
                  'supervisor',
                  'prosecutor',
                  'paralegal',
                  'arraignment_date']


class SchedulingForm(Form):

    def __init__(self, *args, **kwargs):
        super(SchedulingForm, self).__init__()

        case = Case.objects.get(case_number=kwargs['case_num'])

        self.fields['scheduling_date'] = forms.DateTimeField(
            label='Date and Time of the Scheduling Conference',
            input_formats=['%Y-%m-%d %H:%M']
        )

        initial = utils.get_actual_deadline_from_start(case.arraignment_date, SCHEDULING_ORDER_DEADLINE_DAYS)

        self.fields['scheduling_deadline'] = forms.DateTimeField(
            label='Maximum Possible Date',
            initial=initial,
            widget=forms.DateInput(),  # TODO Figure out how to remove time
            input_formats=['%Y-%m-%d']
        )


class TrackForm(Form):
    pass


class TrialForm(Form):
    pass


class OrderForm(Form):
    pass
