from dateutil import parser
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.shortcuts import render, render_to_response
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from remind.models import Deadline
from cases.models import Case, Motion, Judge
from django.core.exceptions import PermissionDenied

from .forms import CaseForm, SchedulingForm, TrackForm, TrialForm, OrderForm, RequestPTIForm, UpdateForm, \
    UpdateCaseForm, UpdateTrackForm, CompleteForm, ExtensionForm, JudgeConfirmedForm, MotionForm, MotionDateForm, \
    MotionResponseForm, MotionFormWithCase, FirstTimeUserForm, ReassignCasesForm
from .constants import TRIAL_DEADLINES, DEADLINE_DESCRIPTIONS, WITNESS_LIST_DEADLINE_DAYS, SUPPORT_EMAIL
from . import utils
from . import case_utils
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.shortcuts import assign_perm


class DashView(LoginRequiredMixin, ListView):
    """Dashboard view for user"""
    template_name = 'remind/dashboard.html'
    component = 'frontend.js'

    def get(self, request, *args, **kwargs):
        # Redirect to first time user page if user does not have a position assigned.
        if request.user.position is None:
            return HttpResponseRedirect(reverse('remind:first-time-user'))
        else:
            return super(DashView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        cases = case_utils.get_cases(self.request.user)
        return case_utils.get_open(cases)

    def get_context_data(self, **kwargs):
        context = super(DashView, self).get_context_data(**kwargs)
        context['component'] = self.component
        context['is_management'] = self.request.user.is_supervisor or self.request.user.is_superuser
        return context


@login_required
def first_time_user(request):
    if request.method == 'POST':
        form = FirstTimeUserForm(request.POST)
        if form.is_valid():
            request.user.position = form.cleaned_data.get('position')
            request.user.save(update_fields=['position'])
            return HttpResponseRedirect(reverse('remind:dashboard'))
    else:
        form = FirstTimeUserForm()
        return render(request, 'remind/first_time_user_form.html', {
            'form': form,
            'support_email': SUPPORT_EMAIL,
        })


################################################################################
# Create Case Sequence

@login_required
def create_case(request, *args, **kwargs):
    """ Case is created on this page, and first deadline for Witness List is set. """
    if request.method == 'POST':
        form = CaseForm(request.POST, *args, **kwargs)

        if form.is_valid():
            # Create case
            data = form.cleaned_data
            case = Case.objects.create(
                created_by=request.user,
                case_number=data.get('case_number'),
                cr_number=data.get('cr_number'),
                defendant=data.get('defendant'),
                judge=data.get('judge'),
                defense_attorney=data.get('defense_attorney'),
                supervisor=data.get('supervisor'),
                prosecutor=data.get('prosecutor'),
                paralegal=data.get('paralegal'),
                secretary=data.get('secretary'),
                victim_advocate=data.get('victim_advocate'),
                arraignment_date=data.get('arraignment_date')
            )

            # Assign permissions
            assign_perm('change_case', case.supervisor, case)
            assign_perm('change_case', case.prosecutor, case)

            if data.get('paralegal'):
                assign_perm('change_case', case.paralegal, case)
            if data.get('secretary'):
                assign_perm('change_case', case.secretary, case)
            if data.get('victim_advocate'):
                assign_perm('change_case', case.victim_advocate, case)

            # Start first deadline for Witness List
            deadline = Deadline.objects.create(
                case=case,
                type=Deadline.WITNESS_LIST,
                datetime=utils.get_actual_deadline_from_start(
                    start_date=case.arraignment_date,
                    days=WITNESS_LIST_DEADLINE_DAYS),
                created_by=request.user
            )
            utils.complete_old_deadline(deadline)

            return HttpResponseRedirect(reverse('remind:case_created', kwargs={'case_number': case.case_number}))

    else:
        form = CaseForm(*args, **kwargs)

    return render(request, 'remind/case_form.html', {'form': form})


@login_required
def case_created(request, *args, **kwargs):
    """ This page confirms that the case was created """

    case = Case.objects.get(case_number=kwargs.get('case_number'))
    witness_deadline = Deadline.objects.get(case=case, type=Deadline.WITNESS_LIST)
    if witness_deadline.status == Deadline.COMPLETED:
        witness_deadline_message = 'However, since this date has already past, this deadline has been marked as ' \
                                   'completed.'
    else:
        witness_deadline_message = ''

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('remind:scheduling', kwargs={'case_number': case.case_number}))

    return render(request, 'remind/case_created.html',
                  {'case_number': case.case_number,
                   'prosecutor': case.prosecutor,
                   'secretary': case.secretary,
                   'supervisor': case.supervisor,
                   'paralegal': case.paralegal,
                   'victim_advocate': case.victim_advocate,
                   'witness_deadline': witness_deadline.datetime.date(),
                   'witness_deadline_message': witness_deadline_message})


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
            deadline = Deadline.objects.create(
                case=case,
                type=Deadline.SCHEDULING_CONFERENCE,
                datetime=case.scheduling_conference_date,
                created_by=request.user
            )
            utils.complete_old_deadline(deadline)
            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        form = SchedulingForm(case_number=kwargs['case_number'])

    return render(request, 'remind/scheduling_form.html', {'form': form})


################################################################################
# Populate Scheduling Order Sequence


@login_required
def scheduling_order_select_case(request, *args, **kwargs):
    """ This page allows the user to select a case to update its track (deadlines) """
    if request.method == 'POST':
        form = UpdateTrackForm(request.POST, user=request.user)

        if form.is_valid():
            return HttpResponseRedirect(reverse('remind:track', kwargs={'case_number': form.cleaned_data['case_number']}))

    else:
        form = UpdateTrackForm(user=request.user)

    return render(request, 'remind/update_track_form.html', {'form': form})


@login_required
def scheduling_order_track(request, *args, **kwargs):
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
            deadline = Deadline.objects.create(
                case=case,
                type=Deadline.REQUEST_PTI,
                datetime=utils.get_actual_deadline_from_start(case.scheduling_conference_date, day_after_request_due),
                created_by=request.user
            )
            utils.complete_old_deadline(deadline)

            return HttpResponseRedirect(reverse('remind:trial', kwargs=kwargs))
    else:
        form = TrackForm(case_number=kwargs['case_number'])

    return render(request, 'remind/track_form.html', {'form': form})


@login_required
def scheduling_order_trial(request, *args, **kwargs):
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
            deadline = Deadline.objects.create(
                case=case,
                type=Deadline.TRIAL,
                datetime=case.trial_date,
                created_by=request.user
            )
            utils.complete_old_deadline(deadline)

            return HttpResponseRedirect(reverse('remind:order', kwargs=kwargs))

    else:
        form = TrialForm(case_number=kwargs['case_number'])

    return render(request, 'remind/trial_form.html', {'form': form})


@login_required
def scheduling_order_deadlines(request, *args, **kwargs):
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
                deadline = Deadline.objects.create(
                    case=case,
                    type=int(key),
                    datetime=form.cleaned_data.get(key),
                    created_by=request.user
                )
                utils.complete_old_deadline(deadline)

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
            deadline = Deadline.objects.create(
                case=case,
                type=Deadline.CONDUCT_PTI,
                datetime=utils.get_actual_deadline_from_start(case.pti_request_date, day_after_request_due),
                created_by=request.user
            )
            utils.complete_old_deadline(deadline)

            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        form = RequestPTIForm(case_number=kwargs['case_number'])

    return render(request, 'remind/request_pti_form.html', {'form': form})


################################################################################
# Update Case Deadlines Sequence


@login_required
def update_select_case(request, *args, **kwargs):
    """ This form asks the user what case they want to update """
    if request.method == 'POST':
        form = UpdateCaseForm(request.POST, user=request.user)

        if form.is_valid():
            return HttpResponseRedirect(reverse('remind:update', kwargs={'case_number': form.cleaned_data['case_number']}))

    else:
        form = UpdateCaseForm(user=request.user)

    return render(request, 'remind/update_case_form.html', {'form': form})


@login_required
def update(request, *args, **kwargs):
    """ The user can update all the deadlines for a case here. """
    case = Case.objects.get(case_number=kwargs.get('case_number'))

    judges = utils.get_judge_choices()
    sorted_judges = utils.sort_choices(choice=str(case.judge), choices=judges)

    if not request.user.has_perm('change_case', case):
        raise PermissionDenied
    if request.method == 'POST':

        # Request QueryDict is immutable, can circumvent this by creating a mutable copy.
        request.POST = request.POST.copy()

        # Have to manually parse all active deadline fields to properly make timezone aware
        # Do we still need to do this?
        for index, deadline in enumerate(Deadline.objects.filter(case=case).order_by('datetime')):
            # Disabled deadlines will not appear in the post request
            if deadline.status == Deadline.ACTIVE:
                key = '{}'.format(index)
                form_value = request.POST[key]

                request.POST[key] = parser.parse(form_value)

        form = UpdateForm(request.POST, case_number=kwargs.get('case_number'))

        if form.is_valid():
            judge_name = judges[int(form.cleaned_data.get('judge')) - 1][1]
            judge_first_name = judge_name.split(' ')[0]
            judge_last_name = judge_name.split(' ')[1]

            if str(case.judge) != judge_name:
                case.judge = Judge.objects.get(
                    first_name=judge_first_name,
                    last_name=judge_last_name
                )
                case.updated_by = request.user
                case.save(update_fields=['judge', 'updated_by'])
                messages.add_message(request, messages.INFO, 'Judge has been changed to {}.'.format(
                    case.judge
                ))

            defense_attorney = form.cleaned_data.get('defense_attorney')
            if case.defense_attorney != defense_attorney:
                case.defense_attorney = defense_attorney
                case.save(update_fields=['defense_attorney'])
                messages.add_message(request, messages.INFO, 'Defense attorney has been changed to {}.'.format(
                    case.defense_attorney
                ))

            for index, deadline in enumerate(Deadline.objects.filter(case=case).order_by('datetime')):
                key = '{}'.format(index)
                completed_key = '{}_completed'.format(index)

                if form.cleaned_data.get(key) is not None and deadline.datetime != form.cleaned_data.get(key):
                    deadline.datetime = form.cleaned_data.get(key)
                    deadline.updated_by = request.user
                    deadline.invalid_notice_sent = False
                    deadline.save(update_fields=['datetime', 'updated_by', 'invalid_notice_sent'])
                    messages.add_message(request, messages.INFO,
                                         '{deadline_desc} date has been changed to {date}.'.format(
                                             deadline_desc=DEADLINE_DESCRIPTIONS[str(deadline.type)].capitalize(),
                                             date=deadline.datetime.strftime('%c')
                                         ))

                if form.cleaned_data.get(completed_key):
                    # append deadline completed message
                    deadline.status = Deadline.COMPLETED
                    deadline.updated_by = request.user
                    deadline.save(update_fields=['status', 'updated_by'])
                    messages.add_message(request, messages.INFO, '{deadline_desc} has been completed.'.format(
                        deadline_desc=DEADLINE_DESCRIPTIONS[str(deadline.type)].capitalize(),
                    ))

            case.updated_by = request.user
            case.save(update_fields=['updated_by'])

            if len(messages.get_messages(request)) == 0:
                return HttpResponseRedirect(reverse('remind:dashboard'))
            else:
                return HttpResponseRedirect(reverse('remind:update_confirm', kwargs={
                    'case_number': case.case_number,
                }))

        else:  # Form is invalid - error handling may go here
            pass

    else:  # Request method is GET
        form = UpdateForm(case_number=kwargs['case_number'])
        pass

    # Render form if code gets to this point
    # Index of the override field will be the last field in the form. Saving this to pass into template
    override_index = len(form.fields)
    disabled = utils.get_disabled_fields(case)
    hidden = utils.get_hidden_fields(case)
    return render(request, 'remind/update_form.html', {
        'form': form,
        'case_number': case.case_number,
        'disabled': disabled,
        'hidden': hidden,
        'judges': sorted_judges,
        'override_index': override_index
    })


@login_required
def update_confirm(request, *args, **kwargs):
    """ This page confirms that the case was created """

    case = Case.objects.get(case_number=kwargs.get('case_number'))

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('remind:dashboard'))

    return render(request, 'remind/update_confirm.html', {
        'case_number': case.case_number,
        'messages': messages.get_messages(request),
    })


################################################################################
# Create Motion Sequence


@login_required
def create_motion_select_case(request, *args, **kwargs):
    """ This form allows the user to record a motion filed for a case. """
    if request.method == 'POST':
        form = MotionForm(request.POST, user=request.user)

        if form.is_valid():
            motion = Motion.objects.create(
                title=form.cleaned_data.get('motion_title'),
                case=Case.objects.get(case_number=form.cleaned_data['case_number']),
                type=form.cleaned_data['motion_type'],
                date_received=form.cleaned_data['date_filed'],
            )
            return HttpResponseRedirect(reverse('remind:motion_deadline', kwargs={'motion_pk': motion.pk}))

    else:
        form = MotionForm(user=request.user)

    return render(request, 'remind/create_motion_form.html', {'form': form})


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
            deadline = Deadline.objects.create(
                type=Deadline.PRETRIAL_MOTION_RESPONSE,
                case=motion.case,
                motion=motion,
                datetime=motion.response_deadline,
            )
            utils.complete_old_deadline(deadline)

            # Create motion hearing deadline
            deadline = Deadline.objects.create(
                type=Deadline.PRETRIAL_MOTION_HEARING,
                case=motion.case,
                motion=motion,
                datetime=motion.date_hearing
            )
            utils.complete_old_deadline(deadline)

            return HttpResponseRedirect(reverse('remind:motion_created', kwargs={'motion_pk': motion.pk}))
    else:
        form = MotionDateForm(motion_pk=kwargs.get('motion_pk'))

    return render(request, 'remind/motion_date_form.html', {'form': form})


@login_required
def motion_created(request, *args, **kwargs):
    """
    Confirmation view displaying results of the newly created motion.
    """
    motion = Motion.objects.get(pk=kwargs.get('motion_pk'))

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('remind:dashboard'))

    return render(request, 'remind/motion_created.html', {
        'motion_title': motion.title,
        'case_number': motion.case.case_number,
        'motion_hearing': motion.date_hearing,
        'motion_response_deadline': motion.response_deadline
    })


################################################################################
# Motion Response Reminder


@login_required
def motion_response(request, *args, **kwargs):
    """
    This form allows the user to record that a motion response was filed.
    The deadline is marked as complete.
    """
    motion = Motion.objects.get(pk=kwargs.get('motion_pk'))
    case = motion.case
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    if request.method == 'POST':
        form = MotionResponseForm(request.POST)
        if form.is_valid():
            motion.response_filed = form.cleaned_data['response_filed']
            motion.save(update_fields=['response_filed'])
            if motion.response_filed is not None:
                deadline = Deadline.objects.get(motion=motion, type=Deadline.PRETRIAL_MOTION_RESPONSE)
                deadline.status = Deadline.COMPLETED
                deadline.save(update_fields=['status'])
            return HttpResponseRedirect(reverse('remind:dashboard'))
    else:
        form = MotionResponseForm()

    return render(
        request,
        'remind/motion_response_form.html', {
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
    deadline = Deadline.objects.get(pk=kwargs.get('deadline_pk'))
    case = deadline.case
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

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
        'remind/complete_form.html', {
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

    deadline = Deadline.objects.get(pk=kwargs.get('deadline_pk'))
    case = deadline.case
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    if request.method == 'POST':
        form = ExtensionForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))
        if form.is_valid():
            deadline.invalid_extension_filed = form.cleaned_data.get('extension_filed')
            deadline.updated_by = request.user
            deadline.save(update_fields=['invalid_extension_filed', 'updated_by'])
            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        # TODO Does this request need to be a POST? Think this is a mistake
        form = ExtensionForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))

    return render(
        request,
        'remind/extension_form.html', {
            'form': form,
            'deadline_desc': DEADLINE_DESCRIPTIONS[str(deadline.type)],
            'case_number': deadline.case.case_number,
            'date': deadline.datetime
        }
    )


@login_required
def judge_confirmed(request, *args, **kwargs):
    """ This page allows the user to record that a judge has approved the extension for a deadline. """

    deadline = Deadline.objects.get(pk=kwargs.get('deadline_pk'))
    case = deadline.case
    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    if request.method == 'POST':
        form = JudgeConfirmedForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))
        if form.is_valid():
            deadline.invalid_judge_approved = form.cleaned_data.get('judge_approved')
            deadline.updated_by = request.user
            deadline.save(update_fields=['invalid_judge_approved', 'updated_by'])
            return HttpResponseRedirect(reverse('remind:dashboard'))

    else:
        # TODO Does this request need to be a POST? Think this is a mistake
        form = JudgeConfirmedForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))

    return render(
        request,
        'remind/judge_confirmed_form.html', {
            'form': form,
            'deadline_desc': DEADLINE_DESCRIPTIONS[str(deadline.type)],
            'case_number': deadline.case.case_number,
            'date': deadline.datetime,
            'required_days': utils.get_deadline_dict(deadline.case.track)[str(deadline.type)]
        }
    )


@login_required
def case_closed(request, *args, **kwargs):
    """Completes all active deadlines on a case and returns a confirmation to the user."""
    case = Case.objects.get(case_number=kwargs.get('case_number'))

    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    utils.close_case(case)

    return render(
        request, 'remind/case_closed.html', {
            'case_number': case.case_number,
            'defendant': case.defendant,
            'support_email': SUPPORT_EMAIL,  # Should this be changed to "your supervisor"?
        }
    )


@login_required
def stay_case(request, *args, **kwargs):
    """Stays a case and and all active deadlines and returns a confirmation to the user"""
    # TODO Prompt user to select reason?
    case = Case.objects.get(case_number=kwargs.get('case_number'))

    if not request.user.has_perm('change_case', case):
        raise PermissionDenied

    utils.stay_case(case)

    return render(
        request, 'remind/case_stayed.html', {
            'case_number': case.case_number,
            'defendant': case.defendant,
        }
    )


@login_required
def resume_case(request, *args, **kwargs):
    case = Case.objects.get(case_number=kwargs.get('case_number'))

    if request.method == 'POST':
        utils.resume_case(case)
        # Should this be treated as a new scheduling order instead of going straight to UpdateView?
        return HttpResponseRedirect(reverse('remind:update', kwargs={'case_number': case.case_number}))

    return render(
        request, 'remind/case_resumed.html', {
            'case_number': case.case_number,
            'defendant': case.defendant,
        }
    )


################################################################################
# Supervisor Action Views


@login_required
def reassign_cases(request, *args, **kwargs):
    """Select a user to reassign cases from"""
    if not request.user.is_supervisor and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = ReassignCasesForm(request.POST)

        if form.is_valid():
            user_to_modify = form.cleaned_data.get('user_to_modify')
            return HttpResponseRedirect(reverse('remind:reassign-cases-with-user',
                                                kwargs={'user_pk': user_to_modify.pk}))

    else:
        form = ReassignCasesForm()

    return render(request, 'remind/reassign_cases_form.html', {'form': form})
