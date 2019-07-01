from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.shortcuts import render, render_to_response
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from .models import Case, Deadline, Motion
from django.core.exceptions import PermissionDenied

from .forms import CaseForm, SchedulingForm, TrackForm, TrialForm, OrderForm, RequestPTIForm, UpdateForm, \
    UpdateCaseForm, UpdateTrackForm, CompleteForm, ExtensionForm, JudgeConfirmedForm, MotionForm, MotionDateForm, \
    MotionResponseForm, MotionFormWithCase
from .constants import TRIAL_DEADLINES, DEADLINE_DESCRIPTIONS, WITNESS_LIST_DEADLINE_DAYS, JUDGES
from . import utils
from . import case_utils
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.shortcuts import assign_perm


class DashView(LoginRequiredMixin, ListView):
    """ Dashboard view for user """

    template_name = 'remind/dashboard.html'

    def get_queryset(self):
        cases = case_utils.get_cases(self.request.user)
        return case_utils.get_open(cases)

    def get_context_data(self, **kwargs):
        context = super(DashView, self).get_context_data(**kwargs)
        cases = case_utils.get_cases(self.request.user)
        closed_cases = case_utils.get_closed(cases)
        context['closed_cases'] = closed_cases
        return context


################################################################################
# Create Case Sequence


class CaseCreateView(LoginRequiredMixin, CreateView):
    """ Case is created on this page, and first deadline for Witness List is set. """
    model = Case
    form_class = CaseForm

    def get_success_url(self):
        self.object.created_by = self.request.user
        judges_dict = dict(JUDGES)
        self.object.judge = judges_dict[int(self.object.judge)]
        self.object.save()
        assign_perm('change_case', self.object.prosecutor, self.object)
        assign_perm('change_case', self.object.secretary, self.object)
        assign_perm('change_case', self.object.supervisor, self.object)

        # Start first deadline for Witness List
        Deadline.objects.create(
            case=self.object,
            type=Deadline.WITNESS_LIST,
            datetime=utils.get_actual_deadline_from_start(
                start_date=self.object.arraignment_date,
                days=WITNESS_LIST_DEADLINE_DAYS),
            created_by=self.request.user
        )

        return reverse('remind:case_created', kwargs={'case_number': self.object.case_number})


class DashView(LoginRequiredMixin, ListView):
    template_name = 'remind/dashboard.html'
    component = 'rulelist.js'

    def get_queryset(self):
        cases = case_utils.get_cases(self.request.user)
        return case_utils.get_open(cases)

    def get_context_data(self, **kwargs):
        context = super(DashView, self).get_context_data(**kwargs)
        context['component'] = self.component
        return context


@login_required
def case_created(request, *args, **kwargs):
    """ This page confirms that the case was created """

    case = Case.objects.get(case_number=kwargs.get('case_number'))
    witness_deadline = Deadline.objects.get(case=case, type=Deadline.WITNESS_LIST)

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('remind:scheduling', kwargs={'case_number': case.case_number}))

    return render(request, 'remind/case_created.html',
                  {'case_number': case.case_number,
                   'prosecutor': case.prosecutor,
                   'secretary': case.secretary,
                   'supervisor': case.supervisor,
                   'witness_deadline': witness_deadline.datetime.date()})


@login_required
def scheduling(request, *args, **kwargs):
    """
    The user sets the date for the scheduling conference here.
    A deadline is created for the scheduling conference.
    """
    case = Case.objects.get(case_number=kwargs.get('case_number'))

    if request.method == 'POST':
        form = SchedulingForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            # Set scheduling conference for date
            case.scheduling_conference_date = form.cleaned_data.get('scheduling_conference_date')
            case.updated_by = request.user
            case.save(update_fields=['scheduling_conference_date', 'updated_by'])

            # Start scheduling conference deadline timer
            Deadline.objects.create(
                case=case,
                type=Deadline.SCHEDULING_CONFERENCE,
                datetime=case.scheduling_conference_date,
                created_by=request.user
            )
            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        form = SchedulingForm(case_number=kwargs['case_number'])

    return render(request, 'remind/scheduling_form.html', {'form': form})


################################################################################
# Populate Scheduling Order Sequence


class UpdateTrackView(LoginRequiredMixin, FormView):
    """ This page allows the user to select a case to update its track (deadlines) """

    template_name = 'remind/update_track_form.html'
    form_class = UpdateTrackForm
    case_number = ''

    def form_valid(self, form):
        self.case_number = form.cleaned_data['case_number']
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('remind:track', kwargs={'case_number': self.case_number})


@login_required
def track(request, *args, **kwargs):
    """
    The user updates the scheduling conference date and sets the track for the case.
    The deadline to request PTIs is also created here.
    """
    case = Case.objects.get(case_number=kwargs.get('case_number'))
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    if request.method == 'POST':
        form = TrackForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            case = Case.objects.get(case_number=kwargs.get('case_number'))

            # Set scheduling conference for date
            case.scheduling_conference_date = form.cleaned_data.get('scheduling_conference_date')
            case.save(update_fields=['scheduling_conference_date'])

            # Set track for case
            # Defining this variable again ensures scheduling_conference_date is saved as a datetime
            case.track = int(form.cleaned_data.get('track'))
            case.updated_by = request.user
            case.save(update_fields=['track', 'updated_by'])

            # Complete scheduling conference deadline timer
            scheduling_conference_deadline = Deadline.objects.get(case=case, type=Deadline.SCHEDULING_CONFERENCE)
            scheduling_conference_deadline.status = Deadline.COMPLETED
            scheduling_conference_deadline.updated_by = request.user
            scheduling_conference_deadline.save(update_fields=['status', 'updated_by'])

            # Start Request PTI deadline timer
            deadlines_dict = utils.get_deadline_dict(case.track)
            day_after_request_due = deadlines_dict[str(Deadline.REQUEST_PTI)] + 1
            Deadline.objects.create(
                case=case,
                type=Deadline.REQUEST_PTI,
                datetime=utils.get_actual_deadline_from_start(case.scheduling_conference_date, day_after_request_due),
                created_by=request.user
            )

            return HttpResponseRedirect(reverse('remind:trial', kwargs=kwargs))
    else:
        form = TrackForm(case_number=kwargs['case_number'])

    return render(request, 'remind/track_form.html', {'form': form})


@login_required
def trial(request, *args, **kwargs):
    """
    The user sets the trial date here.
    A deadline is created for the trial.
    """
    if request.method == 'POST':
        form = TrialForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            # Set scheduling conference for date
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            case.trial_date = form.cleaned_data.get('trial_date')
            case.updated_by = request.user
            case.save(update_fields=['trial_date', 'updated_by'])

            # Start trial deadline timer
            Deadline.objects.create(
                case=case,
                type=Deadline.TRIAL,
                datetime=case.trial_date,
                created_by=request.user
            )

            return HttpResponseRedirect(reverse('remind:order', kwargs=kwargs))

    else:
        form = TrialForm(case_number=kwargs['case_number'])

    return render(request, 'remind/trial_form.html', {'form': form})


@login_required
def order(request, *args, **kwargs):
    """
    The user populates the scheduling order by entering the dates for
    multiple deadlines for the case on this page. A deadline is created
    for each one.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            case.updated_by = request.user
            case.save(update_fields=['updated_by'])
            for key in TRIAL_DEADLINES:
                Deadline.objects.create(
                    case=case,
                    type=int(key),
                    datetime=form.cleaned_data.get(key),
                    created_by=request.user
                )

            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        form = OrderForm(case_number=kwargs['case_number'])

    return render(request, 'remind/order_form.html', {'form': form})


################################################################################
# Request PTI Sequence


@login_required
def request_pti(request, *args, **kwargs):
    """
    The user enters the deadline for the defense to request a PTI here.
    A deadline is created for this.
    """
    if request.method == 'POST':
        form = RequestPTIForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            case.pti_request_date = form.cleaned_data.get('request_pti_date')
            case.updated_by = request.user
            case.save(update_fields=['pti_request_date', 'updated_by'])

            # Defining this variable again ensures pti_request_date is saved as a datetime
            case = Case.objects.get(case_number=kwargs.get('case_number'))

            # Start Conduct PTI deadline timer
            deadlines_dict = utils.get_deadline_dict(case.track)
            day_after_request_due = deadlines_dict[str(Deadline.CONDUCT_PTI)] + 1
            Deadline.objects.create(
                case=case,
                type=Deadline.CONDUCT_PTI,
                datetime=utils.get_actual_deadline_from_start(case.pti_request_date, day_after_request_due),
                created_by=request.user
            )

            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        form = RequestPTIForm(case_number=kwargs['case_number'])

    return render(request, 'remind/request_pti_form.html', {'form': form})


################################################################################
# Update Case Deadlines Sequence


class UpdateCaseView(LoginRequiredMixin, FormView):
    """ This form asks the user what case they want to update """
    template_name = 'remind/update_case_form.html'
    form_class = UpdateCaseForm
    case_number = ''

    def form_valid(self, form):
        self.case_number = form.cleaned_data['case_number']
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('remind:update', kwargs={'case_number': self.case_number})


@login_required
def update(request, *args, **kwargs):
    """ The user can update all the deadlines for a case here. """
    case = Case.objects.get(case_number=kwargs.get('case_number'))
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied
    if request.method == 'POST':

        form = UpdateForm(request.POST, case_number=kwargs.get('case_number'))

        if form.is_valid():
            judge = JUDGES[int(form.cleaned_data.get('judge'))-1][1]
            defense_attorney = form.cleaned_data.get('defense_attorney')

            if case.judge != judge:
                case.judge = judge
                case.updated_by = request.user
                case.save(update_fields=['judge'])

            if case.defense_attorney != form:
                case.defense_attorney = defense_attorney
                case.updated_by = request.user
                case.save(update_fields=['defense_attorney'])

            for index, deadline in enumerate(Deadline.objects.filter(case=case).order_by('datetime')):
                key = '{}'.format(index)
                completed_key = '{}_completed'.format(index)

                if form.cleaned_data.get(key) is not None and deadline.datetime != form.cleaned_data.get(key):
                    deadline.datetime = form.cleaned_data.get(key)
                    deadline.updated_by = request.user
                    deadline.invalid_notice_sent = False
                    deadline.save(update_fields=['datetime', 'updated_by', 'invalid_notice_sent'])

                if form.cleaned_data.get(completed_key):
                    deadline.status = Deadline.COMPLETED
                    deadline.updated_by = request.user
                    deadline.save(update_fields=['status', 'updated_by'])

            case.updated_by = request.user
            case.save(update_fields=['updated_by'])

            return HttpResponseRedirect(reverse('remind:dashboard'))

        else:  # Form is invalid
            # Icky duplicate code
            disabled = [False, False]  # First two fields for judge and defense attorney should not be disabled
            for deadline in Deadline.objects.filter(case=case).order_by('datetime'):
                answer = (deadline.status != Deadline.ACTIVE)
                disabled.append(answer)
                disabled.append(answer)

            return render(request, 'remind/update_form.html',
                          {'form': form,
                           'case_number': case.case_number,
                           'disabled': disabled,
                           'judges': JUDGES,})

    else:
        form = UpdateForm(case_number=kwargs['case_number'])

    # Icky duplicate code
    disabled = [False, False]  # First two fields for judge and defense attorney should not be disabled
    for deadline in Deadline.objects.filter(case=case).order_by('datetime'):
        answer = (deadline.status != Deadline.ACTIVE)
        disabled.append(answer)
        disabled.append(answer)

    return render(request, 'remind/update_form.html',
                  {'form': form, 'case_number': case.case_number, 'disabled': disabled, 'judges': JUDGES})


################################################################################
# Create Motion Sequence


class CreateMotionView(LoginRequiredMixin, FormView):
    """ This form allows the user to record a motion filed for a case. """

    template_name = 'remind/create_motion_form.html'
    form_class = MotionForm
    case_number = ''

    def form_valid(self, form):
        self.motion = Motion.objects.create(
            title=form.cleaned_data.get('motion_title'),
            case=Case.objects.get(case_number=form.cleaned_data['case_number']),
            type=form.cleaned_data['motion_type'],
            date_received=form.cleaned_data['date_filed'],
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('remind:motion_deadline', kwargs={'motion_pk': self.motion.pk})


class CreateMotionViewWithCase(LoginRequiredMixin, FormView):
    """ This is the same form as CreateMotionView, but with a case number already provided. """

    template_name = 'remind/create_motion_form_with_case.html'
    form_class = MotionFormWithCase

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def form_valid(self, form):
        self.motion = Motion.objects.create(
            title=form.cleaned_data.get('motion_title'),
            case=Case.objects.get(case_number=self.kwargs['case_number']),
            type=form.cleaned_data['motion_type'],
            date_received=form.cleaned_data['date_filed'],
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('remind:motion_deadline', kwargs={'motion_pk': self.motion.pk})


def create_motion_with_case(request, *args, **kwargs):


    template_name = 'remind/create_motion_form_with_case.html'
    form_class = MotionFormWithCase
    case = Case.objects.get(case_number=kwargs.get('case_number'))
    form = form_class(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            motion = Motion.objects.create(
                title=form.cleaned_data.get('motion_title'),
                case=case,
                type=form.cleaned_data['motion_type'],
                date_received=form.cleaned_data['date_filed'],
            )
            return HttpResponseRedirect('remind:motion_deadline', kwargs={'motion_pk': motion.pk})

    return render(request, template_name, {'form': form})


@login_required
def motion_deadline(request, *args, **kwargs):
    """
    This form allows the user to record dates for the motion response deadline and hearing.
    Deadlines are created for each of these dates.
    """

    motion = Motion.objects.get(pk=kwargs.get('motion_pk'))
    case = motion.case
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    if request.method == 'POST':
        form = MotionDateForm(request.POST, motion_pk=kwargs.get('motion_pk'))
        if form.is_valid():
            motion = Motion.objects.get(pk=kwargs.get('motion_pk'))
            motion.response_deadline = form.cleaned_data['response_deadline']
            motion.date_hearing = form.cleaned_data['date_hearing']
            motion.save(update_fields=['response_deadline', 'date_hearing'])

            # Create motion response deadline
            Deadline.objects.create(
                type=Deadline.PRETRIAL_MOTION_RESPONSE,
                case=motion.case,
                motion=motion,
                datetime=motion.response_deadline,
            )

            # Create motion hearing deadline
            Deadline.objects.create(
                type=Deadline.PRETRIAL_MOTION_HEARING,
                case=motion.case,
                motion=motion,
                datetime=motion.date_hearing
            )

            return HttpResponseRedirect(reverse('remind:dashboard'))
    else:
        form = MotionDateForm(motion_pk=kwargs.get('motion_pk'))

    return render(request, 'remind/motion_date_form.html', {'form': form})


################################################################################
# Motion Response Reminder


@login_required
def motion_response(request, *args, **kwargs):
    """
    This form allows the user to record that a motion response was filed.
    The deadline is marked as complete.
    """
    case = Case.objects.get(case_number=kwargs.get('case_number'))
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    motion = Motion.objects.get(pk=kwargs.get('motion_pk'))
    form = MotionResponseForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            motion.response_filed = form.cleaned_data['response_filed']
            motion.save(update_fields=['response_filed'])
            if motion.response_filed is not None:
                deadline = Deadline.objects.get(motion=motion, type=Deadline.PRETRIAL_MOTION_RESPONSE)
                deadline.status = Deadline.COMPLETED
                deadline.save(update_fields=['status'])
            return HttpResponseRedirect(reverse('remind:dashboard'))

    return render(
        request,
        'remind/motion_response_form.html',
        {
            'form': form,
            'motion_title': motion.title,
            'case_number': motion.case.case_number,
            'motion_type': Motion.TYPE_CHOICES[motion.type][1],
            'date_received': motion.date_received
        }
    )


################################################################################
# Complete Deadline view


@login_required
def complete(request, *args, **kwargs):
    """
    This page allows the user to mark a deadline as complete.
    """
    case = Case.objects.get(case_number=kwargs.get('case_number'))
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    deadline = Deadline.objects.get(pk=kwargs.get('deadline_pk'))
    if request.method == 'POST':
        form = CompleteForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))
        if form.is_valid():
            if form.cleaned_data.get('completed'):
                deadline.status = Deadline.COMPLETED
                deadline.updated_by = request.user
                deadline.save(update_fields=['status', 'updated_by'])
            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        form = CompleteForm(deadline_pk=kwargs.get('deadline_pk'))

    return render(
        request,
        'remind/complete_form.html',
        {
            'form': form,
            'deadline_desc': DEADLINE_DESCRIPTIONS[str(deadline.type)],
            'case_number': deadline.case.case_number,
            'date': deadline.datetime
        }
    )


################################################################################
# Invalid deadline views


@login_required
def extension(request, *args, **kwargs):
    """ This page allows the user to record that an extension has been filed on a deadline """

    case = Case.objects.get(case_number=kwargs.get('case_number'))
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    deadline = Deadline.objects.get(pk=kwargs.get('deadline_pk'))
    if request.method == 'POST':
        form = ExtensionForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))
        if form.is_valid():
            deadline.invalid_extension_filed = form.cleaned_data.get('extension_filed')
            deadline.updated_by = request.user
            deadline.save(update_fields=['invalid_extension_filed', 'updated_by'])
            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        form = ExtensionForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))

    return render(
        request,
        'remind/extension_form.html',
        {
            'form': form,
            'deadline_desc': DEADLINE_DESCRIPTIONS[str(deadline.type)],
            'case_number': deadline.case.case_number,
            'date': deadline.datetime
        }
    )


@login_required
def judge_confirmed(request, *args, **kwargs):
    """ This page allows the user to record that a judge has approved the extension for a deadline. """

    case = Case.objects.get(case_number=kwargs.get('case_number'))
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    deadline = Deadline.objects.get(pk=kwargs.get('deadline_pk'))
    if request.method == 'POST':
        form = JudgeConfirmedForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))
        if form.is_valid():
            deadline.invalid_judge_approved = form.cleaned_data.get('judge_approved')
            deadline.updated_by = request.user
            deadline.save(update_fields=['invalid_judge_approved', 'updated_by'])
            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        form = JudgeConfirmedForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))

    return render(
        request,
        'remind/judge_confirmed_form.html',
        {
            'form': form,
            'deadline_desc': DEADLINE_DESCRIPTIONS[str(deadline.type)],
            'case_number': deadline.case.case_number,
            'date': deadline.datetime,
            'required_days': utils.get_deadline_dict(deadline.case.track)[str(deadline.type)]
        }
    )
