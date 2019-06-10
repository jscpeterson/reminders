from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form
from .models import Case, Deadline
from users.models import CustomUser
from django import forms
from . import utils
from .constants import SCHEDULING_ORDER_DEADLINE_DAYS, TRIAL_DEADLINES, DEADLINE_DESCRIPTIONS

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


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

    scheduling_conference_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        label='Date and time of the scheduling conference',
    )

    def __init__(self, *args, **kwargs):
        case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)
        initial = utils.get_actual_deadline_from_start(case.arraignment_date, SCHEDULING_ORDER_DEADLINE_DAYS)
        self.fields['scheduling_conference_date'].initial = initial


class TrackForm(Form):

    def __init__(self, *args, **kwargs):
        case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

        initial = case.scheduling_conference_date
        self.fields['scheduling_conference_date'] = forms.DateTimeField(
            label='What did the scheduling conference actually occur?',
            initial=initial,
        )

        self.fields['track'] = forms.ChoiceField(
            choices=Case.TRACK_CHOICES,
            label='What is the case track?',
        )


class TrialForm(Form):

    def __init__(self, *args, **kwargs):
        case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

        deadline_dict = utils.get_deadline_dict(case.track)

        initial = utils.get_actual_deadline_from_start(case.arraignment_date,
                                                       deadline_dict[str(Deadline.TRIAL)])
        self.fields['trial_date'] = forms.DateTimeField(
            label='Date and time of the trial\'s first day',
            initial=initial,
            input_formats=['%Y-%m-%d %H:%M']
        )


class OrderForm(Form):

    def __init__(self, *args, **kwargs):
        case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

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
        case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

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
        case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

        for index, deadline in enumerate(Deadline.objects.filter(case=case,)):
            key = 'deadline_{}'.format(index)
            label = '{expired}{completed}{deadline_desc}'.format(
                expired='(EXPIRED) ' if deadline.status == Deadline.EXPIRED else '',
                completed='(COMPLETED) ' if deadline.status == Deadline.COMPLETED else '',
                deadline_desc=DEADLINE_DESCRIPTIONS[str(deadline.type)].capitalize(),
            )
            initial = deadline.datetime

            self.fields[key] = forms.DateTimeField(
                label=label,
                initial=initial,
                disabled=deadline.status != Deadline.ACTIVE
            )


class UpdateHomeForm(Form):
    case_number = forms.CharField(required=True)
    # FIXME For some reason required=True is not working, an empty field throws a KeyError

    def clean(self):
        cd = self.cleaned_data
        if not Case.objects.filter(case_number=cd['case_number']):
            raise ValidationError('Case not found with this number.')


class CompleteForm(Form):

    def __init__(self, *args, **kwargs):
        deadline_pk = kwargs.pop('deadline_pk')
        super(CompleteForm, self).__init__(*args, **kwargs)

        deadline = Deadline.objects.get(pk=deadline_pk)

        label = 'Has the {desc} on case {case} been completed?'.format(
            desc=DEADLINE_DESCRIPTIONS[str(deadline.type)],
            case=deadline.case.case_number
        )

        self.fields['completed'] = forms.BooleanField(
            label=label,
            required=False
        )


class ExtensionForm(Form):

    def __init__(self, *args, **kwargs):
        deadline_pk = kwargs.pop('deadline_pk')
        super(ExtensionForm, self).__init__(*args, **kwargs)

        self.fields['extension_filed'] = forms.BooleanField(
            label='Have you filed for an extension?',
            required=False
        )


class JudgeConfirmedForm(Form):

    def __init__(self, *args, **kwargs):
        deadline_pk = kwargs.pop('deadline_pk')
        super(JudgeConfirmedForm, self).__init__(*args, **kwargs)

        self.fields['judge_approved'] = forms.BooleanField(
            label='Has this deadline been approved by the judge?',
            required=False
        )
