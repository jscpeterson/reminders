from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, FormView
from .models import Case, Deadline
from .forms import CaseForm, SchedulingForm, TrackForm, TrialForm, OrderForm
from .constants import TRIAL_DEADLINES
from . import utils


class CaseCreate(CreateView):
    model = Case
    form_class = CaseForm

    def get_success_url(self):
        return reverse('scheduling', kwargs={'case_number': self.object.case_number})


class SchedulingView(FormView):

    template_name = 'remind/scheduling_form.html'
    form_class = SchedulingForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

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
        return reverse('track', kwargs=self.kwargs)


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
        case = Case.objects.get(case_number=self.kwargs['case_number'])
        case.track = int(request.POST['track'])
        case.save(update_fields=['track'])

        # Complete scheduling conference deadline timer
        Deadline.objects.filter(case=case, type=Deadline.SCHEDULING_CONFERENCE).delete()

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
            datetime=case.scheduling_conference_date,
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
        # TODO Figure out where to go from here (UpdateView?)
        return


class UpdateView(FormView):
    # TODO Create a form view that displays all the active deadlines on a case, allowing the user to modify them
    pass
