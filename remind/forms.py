from material.forms import ModelForm, Form
from .models import Case, Deadline
from django import forms
from . import utils
from .constants import SCHEDULING_ORDER_DEADLINE_DAYS, TRACK_ONE_DEADLINE_LIMITS, TRACK_TWO_DEADLINE_LIMITS, \
    TRACK_THREE_DEADLINE_LIMITS


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

        self.fields['track'] = forms.ChoiceField(
            choices=Case.TRACK_CHOICES,
            label='What is the case track?',
        )


class TrialForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        if case.track == 1:
            deadlines = TRACK_ONE_DEADLINE_LIMITS
        elif case.track == 2:
            deadlines = TRACK_TWO_DEADLINE_LIMITS
        elif case.track == 3:
            deadlines = TRACK_THREE_DEADLINE_LIMITS
        else:
            raise Exception('Track not valid')

        initial = utils.get_actual_deadline_from_start(case.scheduling_conference_date, deadlines[str(Deadline.TRIAL)])

        self.fields['trial_date'] = forms.DateTimeField(
            label='Trial',
            initial=initial
        )


class OrderForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])
