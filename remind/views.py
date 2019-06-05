from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView
from .models import Case, Deadline
from .forms import CaseForm, SchedulingForm, TrackForm, TrialForm, OrderForm, RequestPTIForm, UpdateForm, \
    UpdateHomeForm, CompleteForm
from .constants import TRIAL_DEADLINES, SOURCE_URL
from . import utils


class CaseCreateView(CreateView):
    model = Case
    form_class = CaseForm

    def get_success_url(self):
        return reverse('scheduling', kwargs={'case_number': self.object.case_number})


def scheduling(request, *args, **kwargs):
    if request.method == 'POST':
        form = SchedulingForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            # Set scheduling conference for date
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            case.scheduling_conference_date = form.cleaned_data.get('scheduling_conference_date')
            case.save(update_fields=['scheduling_conference_date'])

            # Start scheduling conference deadline timer
            Deadline.objects.create(
                case=case,
                type=Deadline.SCHEDULING_CONFERENCE,
                datetime=case.scheduling_conference_date,
            )
            return HttpResponseRedirect(SOURCE_URL)

    else:
        form = SchedulingForm(case_number=kwargs['case_number'])

    return render(request, 'remind/scheduling_form.html', {'form': form})


def track(request, *args, **kwargs):
    if request.method == 'POST':
        form = TrackForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            # Set scheduling conference for date
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            case.scheduling_conference_date = form.cleaned_data.get('scheduling_conference_date')
            case.save(update_fields=['scheduling_conference_date'])

            # Set track for case
            # Defining this variable again ensures scheduling_conference_date is saved as a datetime
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            case.track = int(form.cleaned_data.get('track'))
            case.save(update_fields=['track'])

            # Complete scheduling conference deadline timer
            scheduling_conference_deadline = Deadline.objects.get(case=case, type=Deadline.SCHEDULING_CONFERENCE)
            scheduling_conference_deadline.completed = True
            scheduling_conference_deadline.save(update_fields=['completed'])

            # Start Request PTI deadline timer
            deadlines_dict = utils.get_deadline_dict(case.track)
            day_after_request_due = deadlines_dict[str(Deadline.REQUEST_PTI)] + 1
            Deadline.objects.create(
                case=case,
                type=Deadline.REQUEST_PTI,
                datetime=utils.get_actual_deadline_from_start(case.scheduling_conference_date, day_after_request_due)
            )

            return HttpResponseRedirect(reverse('trial', kwargs=kwargs))
    else:
        form = TrackForm(case_number=kwargs['case_number'])

    return render(request, 'remind/track_form.html', {'form': form})


def trial(request, *args, **kwargs):
    if request.method == 'POST':
        form = TrialForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            # Set scheduling conference for date
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            case.trial_date = form.cleaned_data.get('trial_date')
            case.save(update_fields=['trial_date'])

            # Start trial deadline timer
            Deadline.objects.create(
                case=case,
                type=Deadline.TRIAL,
                datetime=case.trial_date,
            )

            return HttpResponseRedirect(reverse('order', kwargs=kwargs))

    else:
        form = TrialForm(case_number=kwargs['case_number'])

    return render(request, 'remind/trial_form.html', {'form': form})


def order(request, *args, **kwargs):
    if request.method == 'POST':
        form = OrderForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            for key in TRIAL_DEADLINES:
                Deadline.objects.create(
                    case=case,
                    type=int(key),
                    datetime=form.cleaned_data.get(key),
                )

            return HttpResponseRedirect(SOURCE_URL)

    else:
        form = OrderForm(case_number=kwargs['case_number'])

    return render(request, 'remind/trial_form.html', {'form': form})


def request_pti(request, *args, **kwargs):
    if request.method == 'POST':
        form = RequestPTIForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            case = Case.objects.get(case_number=kwargs.get('case_number'))
            case.pti_request_date = form.cleaned_data.get('request_pti_date')
            case.save(update_fields=['pti_request_date'])

            # Defining this variable again ensures pti_request_date is saved as a datetime
            case = Case.objects.get(case_number=kwargs.get('case_number'))

            # Start Conduct PTI deadline timer
            deadlines_dict = utils.get_deadline_dict(case.track)
            day_after_request_due = deadlines_dict[str(Deadline.CONDUCT_PTI)] + 1
            Deadline.objects.create(
                case=case,
                type=Deadline.CONDUCT_PTI,
                datetime=utils.get_actual_deadline_from_start(case.pti_request_date, day_after_request_due)
            )

            return HttpResponseRedirect(SOURCE_URL)

    else:
        form = RequestPTIForm(case_number=kwargs['case_number'])

    return render(request, 'remind/request_pti_form.html', {'form': form})


def update(request, *args, **kwargs):
    if request.method == 'POST':
        form = UpdateForm(request.POST, case_number=kwargs.get('case_number'))
        if form.is_valid():
            case = Case.objects.get(case_number=kwargs.get('case_number'))

            for index, deadline in enumerate(Deadline.objects.filter(case=case)):
                key = 'deadline_{}'.format(index)
                if deadline.datetime.strftime('%Y-%m-%d %H:%M:%S') != form.cleaned_data.get(key):
                    deadline.datetime = form.cleaned_data.get(key)
                    deadline.save(update_fields=['datetime'])

            return HttpResponseRedirect(SOURCE_URL)

    else:
        form = UpdateForm(case_number=kwargs['case_number'])

    return render(request, 'remind/update_form.html', {'form': form})


class UpdateHomeView(FormView):
    template_name = 'remind/update_home_form.html'
    form_class = UpdateHomeForm
    case_number = ''

    def form_valid(self, form):
        self.case_number = form.cleaned_data['case_number']
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('update', kwargs={'case_number': self.case_number})


def complete(request, *args, **kwargs):
    if request.method == 'POST':
        form = CompleteForm(request.POST, deadline_pk=kwargs.get('deadline_pk'))
        if form.is_valid():
            deadline = Deadline.objects.get(pk=kwargs.get('deadline_pk'))
            deadline.completed = form.cleaned_data.get('completed')
            deadline.save(update_fields=['completed'])
            return HttpResponseRedirect(SOURCE_URL)

    else:
        form = CompleteForm(deadline_pk=kwargs.get('deadline_pk'))

    return render(request, 'remind/complete_form.html', {'form': form})

