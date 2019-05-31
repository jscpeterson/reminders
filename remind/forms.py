from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form
from .models import Case, Deadline
from users.models import CustomUser
from django import forms
from . import utils
from .constants import SCHEDULING_ORDER_DEADLINE_DAYS, TRIAL_DEADLINES, DEADLINE_DESCRIPTIONS


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
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        initial = utils.get_actual_deadline_from_start(case.arraignment_date, SCHEDULING_ORDER_DEADLINE_DAYS)
        self.fields['scheduling_conference_date'] = forms.DateTimeField(
            label='Date and time of the scheduling conference',
            initial=initial,
            input_formats=['%Y-%m-%d %H:%M']
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
            initial=initial,
            input_formats=['%Y-%m-%d %H:%M']
        )


class OrderForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        deadline_dict = utils.get_deadline_dict(case.track)

        for key in TRIAL_DEADLINES:
            label = DEADLINE_DESCRIPTIONS[key].capitalize()
            initial = utils.get_actual_deadline_from_end(case.trial_date, deadline_dict[key])
            self.fields[key] = forms.DateTimeField(
                label=label,
                initial=initial,
                input_formats=['%Y-%m-%d %H:%M']
            )


class RequestPTIForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        deadline_dict = utils.get_deadline_dict(case.track)

        initial = utils.get_actual_deadline_from_start(case.scheduling_conference_date,
                                                       deadline_dict[str(Deadline.REQUEST_PTI)])
        self.fields['request_pti_date'] = forms.DateTimeField(
            label='Date that the defense requested pretrial interviews',
            initial=initial,
            input_formats=['%Y-%m-%d']
        )


class UpdateForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        case = Case.objects.get(case_number=kwargs['case_number'])

        for index, deadline in enumerate(Deadline.objects.filter(case=case)):
            key = 'deadline_{}'.format(index)
            label = '{expired}{deadline_desc}'.format(
                expired='(EXPIRED) ' if deadline.expired else '',
                deadline_desc=DEADLINE_DESCRIPTIONS[str(deadline.type)].capitalize(),
            )
            initial = deadline.datetime

            self.fields[key] = forms.DateTimeField(
                label=label,
                initial=initial,
                disabled=deadline.expired
            )


class UpdateHomeForm(Form):
    case_number = forms.CharField(required=True)
    # FIXME For some reason required=True is not working, an empty field throws a KeyError

    def clean(self):
        cd = self.cleaned_data
        if not Case.objects.filter(case_number=cd['case_number']):
            raise ValidationError('Case not found with this number.')
