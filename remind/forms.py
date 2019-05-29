from material.forms import ModelForm, Form
from .models import Case, Deadline
from django import forms
from . import utils
from .constants import SCHEDULING_ORDER_DEADLINE_DAYS, TRIAL_DEADLINES


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
            label='Date and time of the scheduling conference',
            initial=initial
        )


class TrackForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        initial = case.scheduling_conference_date
        self.fields['scheduling_conference_date'] = forms.DateTimeField(
            label='What did the scheduling conference actually occur?',
            initial=initial
        )

        self.fields['track'] = forms.ChoiceField(
            choices=Case.TRACK_CHOICES,
            label='What is the case track?',
        )


class TrialForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        deadline_dict = utils.get_deadline_dict(case.track)

        initial = utils.get_actual_deadline_from_start(case.scheduling_conference_date,
                                                       deadline_dict[str(Deadline.TRIAL)])
        self.fields['trial_date'] = forms.DateTimeField(
            label='Date and time of the trial\'s first day',
            initial=initial
        )


class OrderForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        deadline_dict = utils.get_deadline_dict(case.track)

        for key, label in TRIAL_DEADLINES.items():
            initial = utils.get_actual_deadline_from_end(case.trial_date, deadline_dict[key])
            self.fields[key] = forms.DateTimeField(
                label=label,
                initial=initial
            )
