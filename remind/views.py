from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, FormView
from .models import Case, Deadline
from .forms import CaseForm, SchedulingForm, TrackForm, TrialForm, OrderForm, RequestPTIForm, UpdateForm, \
    UpdateHomeForm, CompleteForm, ExtensionForm, JudgeConfirmedForm
from .constants import TRIAL_DEADLINES, SOURCE_URL, DEADLINE_DESCRIPTIONS
from . import utils


class CaseCreateView(CreateView):
    model = Case
    form_class = CaseForm

    def get_success_url(self):
        return reverse('scheduling', kwargs={'case_number': self.object.case_number})


class SchedulingView(FormView):
    template_name = 'remind/scheduling_form.html'
    form_class = SchedulingForm

    def get_initial(self):
        return super().get_initial()

    def get_prefix(self):
        return super().get_prefix()

    def get_form_class(self):
        return super().get_form_class()

    def get_form(self, form_class=SchedulingForm):
        return super().get_form(form_class)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def form_valid(self, form):
        super(SchedulingView, self).form_valid()
    
    def form_invalid(self, form):
        super(SchedulingView, self).form_invalid()

    def post(self, request, *args, **kwargs):
        # Set scheduling conference for date
        case = Case.objects.get(case_number=self.kwargs['case_number'])
        case.scheduling_conference_date = request.POST['scheduling_conference_date']
        case.save(update_fields=['scheduling_conference_date'])

        # Start scheduling conference deadline timer
        Deadline.objects.create(
            case=case,
            type=Deadline.SCHEDULING_CONFERENCE,
            datetime=case.scheduling_conference_date,
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return SOURCE_URL


class TrackView(FormView):
    template_name = 'remind/track_form.html'
    form_class = TrackForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def post(self, request, *args, **kwargs):
        # Update scheduling conference date
        case = Case.objects.get(case_number=self.kwargs['case_number'])
        case.scheduling_conference_date = request.POST['scheduling_conference_date']
        case.save(update_fields=['scheduling_conference_date'])

        # Set track for case
        # Defining this variable again ensures scheduling_conference_date is saved as a datetime
        case = Case.objects.get(case_number=self.kwargs['case_number'])
        case.track = int(request.POST['track'])
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

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('trial', kwargs=self.kwargs)


class TrialView(FormView):
    template_name = 'remind/trial_form.html'
    form_class = TrialForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def post(self, request, *args, **kwargs):
        # Set trial date for case
        case = Case.objects.get(case_number=self.kwargs['case_number'])
        case.trial_date = request.POST['trial_date']
        case.save(update_fields=['trial_date'])

        # Start trial deadline timer
        Deadline.objects.create(
            case=case,
            type=Deadline.TRIAL,
            datetime=case.trial_date,
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('order', kwargs=self.kwargs)


class OrderView(FormView):
    template_name = 'remind/order_form.html'
    form_class = OrderForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def post(self, request, *args, **kwargs):
        case = Case.objects.get(case_number=self.kwargs['case_number'])

        for key in TRIAL_DEADLINES:
            Deadline.objects.create(
                case=case,
                type=int(key),
                datetime=request.POST[key],
            )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return SOURCE_URL


class RequestPTIView(FormView):
    template_name = 'remind/request_pti_form.html'
    form_class = RequestPTIForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def post(self, request, *args, **kwargs):
        # Set Request PTI date
        case = Case.objects.get(case_number=self.kwargs['case_number'])
        case.pti_request_date = request.POST['request_pti_date']
        case.save(update_fields=['pti_request_date'])

        # Defining this variable again ensures pti_request_date is saved as a datetime
        case = Case.objects.get(case_number=self.kwargs['case_number'])

        # Start Conduct PTI deadline timer
        deadlines_dict = utils.get_deadline_dict(case.track)
        day_after_request_due = deadlines_dict[str(Deadline.CONDUCT_PTI)] + 1
        Deadline.objects.create(
            case=case,
            type=Deadline.CONDUCT_PTI,
            datetime=utils.get_actual_deadline_from_start(case.pti_request_date, day_after_request_due)
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return SOURCE_URL


class UpdateView(FormView):
    template_name = 'remind/update_form.html'
    form_class = UpdateForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['case_number'] = self.kwargs['case_number']
        return context

    def post(self, request, *args, **kwargs):
        case = Case.objects.get(case_number=self.kwargs['case_number'])

        for index, deadline in enumerate(Deadline.objects.filter(case=case)):
            key = 'deadline_{}'.format(index)
            if deadline.datetime.strftime('%Y-%m-%d %H:%M:%S') != request.POST[key]:
                deadline.datetime = request.POST[key]
                deadline.save(update_fields=['datetime'])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return SOURCE_URL


class UpdateHomeView(FormView):
    template_name = 'remind/update_home_form.html'
    form_class = UpdateHomeForm
    case_number = ''

    def form_valid(self, form):
        self.case_number = form.cleaned_data['case_number']
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('update', kwargs={'case_number': self.case_number})


class CompleteView(FormView):
    template_name = 'remind/complete_form.html'
    form_class = CompleteForm

    def get_form_kwargs(self):
        return self.kwargs

    def post(self, request, *args, **kwargs):
        deadline = Deadline.objects.get(pk=self.kwargs['deadline_pk'])
        deadline.completed = request.POST['completed']
        deadline.save(update_fields=['completed'])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return SOURCE_URL


class ExtensionView(FormView):
    template_name = 'remind/extension_form.html'
    form_class = ExtensionForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        deadline = Deadline.objects.get(pk=self.kwargs['deadline_pk'])
        context['deadline_desc'] = DEADLINE_DESCRIPTIONS[str(deadline.type)]
        context['case_number'] = deadline.case.case_number
        context['date'] = deadline.datetime
        return context

    def post(self, request, *args, **kwargs):
        deadline = Deadline.objects.get(pk=self.kwargs['deadline_pk'])
        deadline.invalid_extension_filed = request.POST['extension_filed']
        deadline.save(update_fields=['invalid_extension_filed'])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return SOURCE_URL


class JudgeConfirmedView(FormView):
    template_name = 'remind/judge_confirmed_form.html'
    form_class = JudgeConfirmedForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        deadline = Deadline.objects.get(pk=self.kwargs['deadline_pk'])
        context['deadline_desc'] = DEADLINE_DESCRIPTIONS[str(deadline.type)]
        context['case_number'] = deadline.case.case_number
        context['date'] = deadline.datetime
        required_days = utils.get_deadline_dict(deadline.case.track)[str(deadline.type)]
        context['required_days'] = required_days
        return context

    def post(self, request, *args, **kwargs):
        deadline = Deadline.objects.get(pk=self.kwargs['deadline_pk'])
        deadline.invalid_judge_approved = request.POST['judge_approved']
        deadline.save(update_fields=['invalid_judge_approved'])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return SOURCE_URL
