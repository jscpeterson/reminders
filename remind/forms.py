import re

from django.db.models import Q
from django.forms import Form

from cases.models import Case, Motion, Judge
from remind.models import Deadline
from datetime import datetime
from users.models import CustomUser
from django import forms
from . import utils
from .constants import SCHEDULING_ORDER_DEADLINE_DAYS, TRIAL_DEADLINES, DEADLINE_DESCRIPTIONS, EVENT_DEADLINES, \
    SECOND_JUDICIAL_DISTRICT

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class FirstTimeUserForm(Form):

    def __init__(self, *args, **kwargs):
        super(FirstTimeUserForm, self).__init__(*args, **kwargs)

        self.fields['position'] = forms.ChoiceField(
            label='Select a position',
            choices=CustomUser.POSITION_CHOICES,
            required=True,
        )


class CaseForm(Form):

    def __init__(self, *args, **kwargs):

        super(CaseForm, self).__init__(*args, **kwargs)
        self.fields['case_number'] = forms.CharField(
            label='DA Case #',
            help_text='Enter a case number with a format similar to DA-{year}-00000. Year should be current.'.format(
                year=datetime.now().year
            ),
            required=True,
        )
        self.fields['cr_number'] = forms.CharField(
            label='CR #',
            help_text='Enter a CR number with a format similar to D-202-AA-2019-00000. Year should be current.',
            required=True,
        )
        self.fields['override'] = forms.BooleanField(label="Ignore invalid case number formatting?", required=False)
        self.fields['defendant'] = forms.CharField(
            required=True,
        )
        self.fields['defense_attorney'] = forms.CharField(
            required=False,
        )
        self.fields['judge'] = forms.ModelChoiceField(
            queryset=Judge.objects.order_by('last_name'),
            required=True,
        )
        self.fields['supervisor'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(is_supervisor=True).order_by('last_name'),
            required=True,
        )
        self.fields['prosecutor'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(position=CustomUser.PROSECUTOR).order_by('last_name'),
            required=True,
        )
        self.fields['paralegal'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(position=CustomUser.PARALEGAL).order_by('last_name'),
            required=False,
        )
        self.fields['secretary'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(position=CustomUser.SECRETARY).order_by('last_name'),
            required=False,
        )
        self.fields['victim_advocate'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(position=CustomUser.VICTIM_ADVOCATE).order_by('last_name'),
            required=False,
        )
        self.fields['arraignment_date'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            required=True,
        )

    def clean(self):
        cleaned_data = super(CaseForm, self).clean()

        case_number = cleaned_data.get('case_number')
        cr_number = cleaned_data.get('cr_number')

        current_year = datetime.now().year

        if case_number:
            # Check case_number exists
            if Case.objects.filter(case_number=case_number).exists():
                self.add_error(
                    'case_number',
                    ' Case with this DA case number already exists.'
                )

            # Check DA Case # pattern
            case_number_format = r'^DA-\D?{year}-\d{{5}}(-\w*)?(-\w*)?$'.format(
                year=current_year
            )
            case_number_pattern = re.compile(case_number_format)

            if not self.cleaned_data.get('override') and not bool(re.match(case_number_pattern, case_number)):
                self.add_error(
                    'case_number',
                    ' DA case number looks invalid. '
                    'Check "Ignore invalid case number formatting?" if you want to use it anyway. '
                )

        if cr_number:
            # Check CR# exists
            if Case.objects.filter(cr_number=cr_number).exists():
                self.add_error(
                    'cr_number',
                    ' Case with this CR# already exists.'
                )

            # Check CR# pattern
            cr_number_format = r'^D-{district}-\D{{2}}-{year}-\d{{5}}$'.format(
                district=SECOND_JUDICIAL_DISTRICT,
                year=current_year,
            )
            cr_number_pattern = re.compile(cr_number_format)

            if cr_number != '' and not self.cleaned_data.get('override') and not bool(re.match(cr_number_pattern, cr_number)):
                self.add_error(
                    'cr_number',
                    ' CR# looks invalid. '
                    'Check "Ignore invalid case number formatting?" if you want to use it anyway. '
                )


class MotionForm(Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MotionForm, self).__init__(*args, **kwargs)
        queryset = utils.filter_cases_by_user_permissions(
            Case.objects.exclude(trial_date__isnull=True), user
        )

        self.fields['case'] = forms.ModelChoiceField(
            queryset=queryset,
            help_text='Only cases with a scheduling order will appear here.'
        )

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

        initial_response = utils.get_motion_response_deadline(self.motion)

        self.fields['response_deadline'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d'],
            label='Deadline to file a response',
            initial=initial_response
        )

        self.fields['override'] = forms.BooleanField(
            label='Ignore invalid dates?',
            required=False,
        )

    def clean(self):
        super(MotionDateForm, self).clean()
        cleaned_data = super().clean()

        if cleaned_data.get('override'):
            return

        if 'response_deadline' in cleaned_data:
            response_deadline = cleaned_data.get('response_deadline')

            if utils.is_motion_response_deadline_invalid(self.motion, response_deadline):
                self.add_error(
                    'response_deadline',
                    'Response deadline is past permissible limit'
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
        label='Ignore invalid date?',
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

        initial = utils.get_actual_deadline_from_start(
            self.case.arraignment_date,
            deadline_dict[str(Deadline.TRIAL)]
        )

        self.fields['trial_date'] = forms.DateTimeField(
            label='Date and time of the trial\'s first day',
            initial=initial,
            input_formats=['%Y-%m-%d %H:%M']
        )

        self.fields['override'] = forms.BooleanField(
            label='Ignore invalid date?',
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
                initial=utils.set_default_deadline_time(initial),
                input_formats=['%Y-%m-%d %H:%M']
            )

        self.fields['override'] = forms.BooleanField(
            label='Ignore invalid dates?',
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

        initial = utils.get_actual_deadline_from_start(
            case.scheduling_conference_date,
            deadline_dict[str(Deadline.REQUEST_PTI)]
        )
        self.fields['request_pti_date'] = forms.DateTimeField(
            label='Date that the defense requested pretrial interviews',
            initial=initial,
            input_formats=['%Y-%m-%d']
        )


class UpdateForm(Form):

    def __init__(self, *args, **kwargs):
        self.case = Case.objects.get(case_number=kwargs.pop('case_number'))
        super().__init__(*args, **kwargs)

        judges = utils.get_judge_choices()
        initial_judge = utils.find_choice_index(choice=str(self.case.judge), choices=judges)
        self.fields['judge'] = forms.ChoiceField(
            choices=judges,
            required=False,
            initial=initial_judge,
            label='Change the judge for this case?',
            disabled=False
        )

        self.fields['defense_attorney'] = forms.CharField(
            required=False,
            initial=self.case.defense_attorney,
            label='Change the defense attorney for this case?',
            disabled=False,
        )

        for index, deadline in enumerate(Deadline.objects.filter(case=self.case).order_by('datetime')):
            key = '{}'.format(index)
            completed_key = '{}_completed'.format(index)
            if deadline.type in [Deadline.PRETRIAL_MOTION_RESPONSE]:
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
            initial = deadline.datetime
            self.fields[key] = forms.DateTimeField(
                label=label,
                initial=initial,
                required=False
            )
            self.fields[completed_key] = forms.BooleanField(
                label="Completed?",
                required=False,
            )

        self.fields['override'] = forms.BooleanField(
            label='Ignore invalid dates?',
            required=False,
        )

    def clean(self):
        cleaned_data = super(UpdateForm, self).clean()

        # check if user both changed a date and marked it as a complete
        # cannot think of a reason they would want to do this so considering it a data entry error
        for index, deadline in enumerate(Deadline.objects.filter(case=self.case).order_by('datetime')):
            key = '{}'.format(index)
            key_completed = '{}_completed'.format(index)

            if deadline.datetime != cleaned_data.get(key) and cleaned_data.get(key_completed):
                self.add_error(
                    key,
                    'Cannot complete a deadline and change it at the same time.'
                )

        # check if overriding invalid dates before doing date validation
        if cleaned_data.get('override'):
            return

        # check deadlines
        for index, deadline in enumerate(Deadline.objects.filter(case=self.case).order_by('datetime')):
            key = '{}'.format(index)

            # check if deadline has been changed and deadline is not inactive
            if cleaned_data.get(key) is not None and deadline.datetime != cleaned_data.get(
                    key) and deadline.status == Deadline.ACTIVE:
                deadline.datetime = cleaned_data.get(key)  # temporarily changing this should be fine if we're never
                # actually saving it

                if utils.is_deadline_invalid(deadline):
                    self.add_error(
                        key,
                        'Deadline outside permissible limits.'
                    )


class UpdateCaseForm(Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UpdateCaseForm, self).__init__(*args, **kwargs)
        queryset = utils.filter_cases_by_user_permissions(
            Case.objects.all(), user
        ).order_by('defendant')

        self.fields['case'] = forms.ModelChoiceField(
            queryset=queryset,
        )


class CompleteForm(Form):

    def __init__(self, *args, **kwargs):
        deadline_pk = kwargs.pop('deadline_pk')
        super(CompleteForm, self).__init__(*args, **kwargs)

        self.deadline = Deadline.objects.get(pk=deadline_pk)

        label = 'Task completed'

        self.fields['completed'] = forms.BooleanField(
            label=label,
            required=False
        )

    def clean(self):
        cleaned_data = super(CompleteForm, self).clean()

        if self.deadline.type in EVENT_DEADLINES:
            self.add_error(
                'completed',
                'This is an event, you do not need to complete it.'
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateTrackForm, self).__init__(*args, **kwargs)
        queryset = utils.filter_cases_by_user_permissions(
            Case.objects.exclude(trial_date__isnull=False), user
        )

        self.fields['case'] = forms.ModelChoiceField(
            queryset=queryset,
            help_text='Only cases without a scheduling order will appear here.',
        )


class ReassignCasesForm(Form):

    def __init__(self, *args, **kwargs):
        super(ReassignCasesForm, self).__init__(*args, **kwargs)

        self.fields['user_to_modify'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.order_by('last_name'),
            label="Select a user whose cases will be moved",
        )


class ReassignCasesWithUserForm(Form):

    def __init__(self, *args, **kwargs):
        user_to_modify = kwargs.pop('user_to_modify')
        super(ReassignCasesWithUserForm, self).__init__(*args, **kwargs)

        # TODO Iterate over an ALL_POSITIONS list for better maintainability
        self.fields['supervisor'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(is_supervisor=True).order_by('last_name'),
            label="Select a new supervisor.",
            required=False,
        )
        self.fields['prosecutor'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(position=CustomUser.PROSECUTOR).order_by('last_name'),
            label="Select a new prosecutor.",
            required=False,
        )
        self.fields['paralegal'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(position=CustomUser.PARALEGAL).order_by('last_name'),
            label="Select a new paralegal.",
            required=False,
        )
        self.fields['secretary'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(position=CustomUser.SECRETARY).order_by('last_name'),
            label="Select a new secretary.",
            required=False,
        )
        self.fields['victim_advocate'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(position=CustomUser.VICTIM_ADVOCATE).order_by('last_name'),
            label="Select a new victim advocate.",
            required=False,
        )

        for index, case in enumerate(Case.objects.filter(
                    Q(supervisor=user_to_modify) |
                    Q(prosecutor=user_to_modify) |
                    Q(secretary=user_to_modify) |
                    Q(paralegal=user_to_modify) |
                    Q(victim_advocate=user_to_modify)
                )):
            self.fields['case_{}'.format(index)] = forms.BooleanField(
                label='{case_number}: {defendant}'.format(case_number=case.case_number, defendant=case.defendant),
                required=False,
            )
