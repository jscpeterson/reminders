from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form
from .models import Case, Deadline, Motion
from datetime import timedelta
from users.models import CustomUser
from django import forms
from . import utils
from .constants import SCHEDULING_ORDER_DEADLINE_DAYS, TRIAL_DEADLINES, DEADLINE_DESCRIPTIONS, JUDGES

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class CaseForm(ModelForm):
    supervisor = forms.ModelChoiceField(queryset=CustomUser.objects.filter(position=1), empty_label=None)
    prosecutor = forms.ModelChoiceField(queryset=CustomUser.objects.filter(position=2), empty_label=None)
    secretary = forms.ModelChoiceField(queryset=CustomUser.objects.filter(position=3), empty_label=None)
    arraignment_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
    case_number = forms.CharField(label='CR#')
    judge = forms.ChoiceField(choices=JUDGES, )

    class Meta:
        model = Case
        fields = ['case_number',
                  'defendant',
                  'judge',
                  'defense_attorney',
                  'supervisor',
                  'prosecutor',
                  'secretary',
                  'arraignment_date']


class MotionForm(Form):

    motion_title = forms.CharField(
        label='Title of the motion'
    )

    case_number = forms.ModelChoiceField(
        queryset=Case.objects.exclude(trial_date__isnull=True),
    )

    date_filed = forms.DateTimeField(
        input_formats=['%Y-%m-%d'],
        label='Date motion was filed'
    )

    motion_type = forms.ChoiceField(
        choices=Motion.TYPE_CHOICES,
        label='Type of motion'
    )


class MotionFormWithCase(Form):

    motion_title = forms.CharField(
        label='Title of the motion'
    )

    date_filed = forms.DateTimeField(
        input_formats=['%Y-%m-%d'],
        label='Date motion was filed'
    )

    motion_type = forms.ChoiceField(
        choices=Motion.TYPE_CHOICES,
        label='Type of motion'
    )


class MotionDateForm(Form):

    def __init__(self, *args, **kwargs):
        self.motion = Motion.objects.get(pk=kwargs.pop('motion_pk'))
        super(MotionDateForm, self).__init__(*args, **kwargs)

        deadline_dict = utils.get_deadline_dict(self.motion.case.track)

        initial_response = utils.get_actual_deadline_from_start(self.motion.date_received, 10)
        initial_hearing = utils.get_actual_deadline_from_end(self.motion.case.trial_date,
                                                             deadline_dict[str(Deadline.PRETRIAL_MOTION_HEARING)], )

        self.fields['response_deadline'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d'],
            label='Deadline to file a response',
            initial=initial_response
        )

        self.fields['date_hearing'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            label='Date of the hearing',
            initial=initial_hearing
        )

        self.fields['override'] = forms.BooleanField(
            label='Override invalid dates?',
            required=False,
        )

    def clean(self):
        super(MotionDateForm, self).clean()
        cleaned_data = super().clean()

        if cleaned_data.get('override'):
            return

        deadline_dict = utils.get_deadline_dict(self.motion.case.track)

        if 'response_deadline' in cleaned_data:
            response_deadline = cleaned_data.get('response_deadline')

            # if not utils.is_deadline_within_limits(
            #     deadline=scheduling_conf_date,
            #     event=self.case.arraignment_date,
            #     days=SCHEDULING_ORDER_DEADLINE_DAYS,
            #     future_event=False,
            # ):
            #     self.add_error(
            #         'scheduling_conference_date',
            #         'Scheduling conference date is past permissible limit'
            #     )

        if 'date_hearing' in cleaned_data:
            date_hearing = cleaned_data.get('date_hearing')

            if not utils.is_deadline_within_limits(
                    deadline=date_hearing,
                    event=self.motion.case.trial_date,
                    days=deadline_dict[str(Deadline.PRETRIAL_MOTION_HEARING)],
                    future_event=True,
            ):
                self.add_error(
                    'date_hearing',
                    'Hearing date is past permissible limit'
                )


class MotionResponseForm(Form):
    response_filed = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        label='Date response was filed'
    )


class SchedulingForm(Form):
    scheduling_conference_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        label='Date and time of the scheduling conference',
        required=True
    )
    override = forms.BooleanField(
        label='Override invalid date?',
        initial=False,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)
        initial = utils.get_actual_deadline_from_start(self.case.arraignment_date, SCHEDULING_ORDER_DEADLINE_DAYS)
        self.fields['scheduling_conference_date'].initial = initial

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('override'):
            return

        if 'scheduling_conference_date' in cleaned_data:
            scheduling_conf_date = cleaned_data.get('scheduling_conference_date')

            if scheduling_conf_date < self.case.arraignment_date:
                self.add_error(
                    'scheduling_conference_date',
                    'Scheduling conference cannot happen before arraignment'
                )

            else:
                if not utils.is_deadline_within_limits(
                        deadline=scheduling_conf_date,
                        event=self.case.arraignment_date,
                        days=SCHEDULING_ORDER_DEADLINE_DAYS,
                        future_event=False,
                ):
                    self.add_error(
                        'scheduling_conference_date',
                        'Scheduling conference date is past permissible limit'
                    )


class TrackForm(Form):

    def __init__(self, *args, **kwargs):
        case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

        initial = Deadline.objects.get(case=case, type=Deadline.SCHEDULING_CONFERENCE).datetime
        self.fields['scheduling_conference_date'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            label='When did the scheduling conference actually occur?',
            initial=initial,
        )

        self.fields['track'] = forms.ChoiceField(
            choices=Case.TRACK_CHOICES,
            label='What is the case track?',
        )


class TrialForm(Form):

    def __init__(self, *args, **kwargs):
        self.case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

        deadline_dict = utils.get_deadline_dict(self.case.track)

        initial = utils.get_actual_deadline_from_start(self.case.arraignment_date,
                                                       deadline_dict[str(Deadline.TRIAL)])
        self.fields['trial_date'] = forms.DateTimeField(
            label='Date and time of the trial\'s first day',
            initial=initial,
            input_formats=['%Y-%m-%d %H:%M']
        )

        self.fields['override'] = forms.BooleanField(
            label='Override invalid date?',
            initial=False,
            required=False,
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('override'):
            return

        if 'trial_date' in cleaned_data:
            trial_date = cleaned_data.get('trial_date')

            if trial_date < self.case.scheduling_conference_date:
                self.add_error(
                    'trial_date',
                    'Trial cannot happen before scheduling conference'
                )

            else:
                deadline_dict = utils.get_deadline_dict(self.case.track)

                # Will raise error even if permissible with extension
                if not utils.is_deadline_within_limits(
                        deadline=trial_date,
                        event=self.case.arraignment_date,
                        days=deadline_dict[str(Deadline.TRIAL)],
                        future_event=False
                ):
                    self.add_error(
                        'trial_date',
                        'Trial date is past permissible limit'
                    )


class OrderForm(Form):
    case = ''

    def __init__(self, *args, **kwargs):
        self.case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

        deadline_dict = utils.get_deadline_dict(self.case.track)

        for key in TRIAL_DEADLINES:
            label = DEADLINE_DESCRIPTIONS[key].capitalize()
            initial = utils.get_actual_deadline_from_end(self.case.trial_date, deadline_dict[key])
            self.fields[key] = forms.DateTimeField(
                label=label,
                initial=initial,
                input_formats=['%Y-%m-%d %H:%M']
            )

        self.fields['override'] = forms.BooleanField(
            label='Override invalid dates?',
            initial=False,
            required=False,
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('override'):
            return

        deadline_dict = utils.get_deadline_dict(self.case.track)

        for key in TRIAL_DEADLINES:
            deadline = cleaned_data.get(key)

            if not utils.is_deadline_within_limits(
                    deadline=deadline,
                    event=self.case.trial_date,
                    days=deadline_dict[key],
                    future_event=True
            ):
                self.add_error(
                    key,
                    'Deadline is past permissible limit'
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

        self.fields['judge'] = forms.CharField(  # TODO Change to choice field
            # choices=JUDGES,
            required=False,
            initial=case.judge, # TODO Change to location in JUDGES dict
            label='Change the judge for this case?',
            disabled=False
        )

        self.fields['defense_attorney'] = forms.CharField(
            required=False,
            initial=case.defense_attorney,
            label='Change the defense attorney for this case?',
            disabled=False
        )

        for index, deadline in enumerate(Deadline.objects.filter(case=case).order_by('datetime')):
            key = '{}'.format(index)
            if deadline.type in [Deadline.PRETRIAL_MOTION_RESPONSE, Deadline.PRETRIAL_MOTION_HEARING]:
                label = '{expired}{completed}{deadline_desc} for {motion_title}'.format(
                    expired='(EXPIRED) ' if deadline.status == Deadline.EXPIRED else '',
                    completed='(COMPLETED) ' if deadline.status == Deadline.COMPLETED else '',
                    deadline_desc=DEADLINE_DESCRIPTIONS[str(deadline.type)].capitalize(),
                    motion_title=deadline.motion.title,
                    required=False
                )
            else:
                label = '{expired}{completed}{deadline_desc}'.format(
                    expired='(EXPIRED) ' if deadline.status == Deadline.EXPIRED else '',
                    completed='(COMPLETED) ' if deadline.status == Deadline.COMPLETED else '',
                    deadline_desc=DEADLINE_DESCRIPTIONS[str(deadline.type)].capitalize(),
                    required=False,
                )
            initial = deadline.datetime.strftime('%Y-%m-%d %H:%M')
            self.fields[key] = forms.DateTimeField(
                input_formats=['%Y-%m-%d %H:%M'],
                label=label,
                initial=initial,
                required=False
            )
            self.fields[key + '_completed'] = forms.BooleanField(
                label="Completed?",
                required=False,
            )


class UpdateCaseForm(Form):
    case_number = forms.ModelChoiceField(
        queryset=Case.objects.all(),
    )


class CompleteForm(Form):

    def __init__(self, *args, **kwargs):
        deadline_pk = kwargs.pop('deadline_pk')
        super(CompleteForm, self).__init__(*args, **kwargs)

        deadline = Deadline.objects.get(pk=deadline_pk)

        label = 'Task completed'

        self.fields['completed'] = forms.BooleanField(
            label=label,
            required=False
        )


class ExtensionForm(Form):

    def __init__(self, *args, **kwargs):
        deadline_pk = kwargs.pop('deadline_pk')
        super(ExtensionForm, self).__init__(*args, **kwargs)

        self.fields['extension_filed'] = forms.BooleanField(
            label='Extension filed',
            required=False
        )


class JudgeConfirmedForm(Form):

    def __init__(self, *args, **kwargs):
        deadline_pk = kwargs.pop('deadline_pk')
        super(JudgeConfirmedForm, self).__init__(*args, **kwargs)

        self.fields['judge_approved'] = forms.BooleanField(
            label='Judge approved',
            required=False
        )


class UpdateTrackForm(Form):
    case_number = forms.ModelChoiceField(
        queryset=Case.objects.all(),
    )
