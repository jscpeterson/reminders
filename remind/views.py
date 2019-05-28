from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, FormView
from .models import Case
from .forms import CaseForm, SchedulingForm, TrackForm, TrialForm, OrderForm


class CaseCreate(CreateView):
    model = Case
    form_class = CaseForm

    def get_success_url(self):
        return reverse('scheduling', kwargs={'case_number': self.object.case_number})


class SchedulingView(FormView):

    template_name = 'remind/scheduling_form.html'
    form_class = SchedulingForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        case = Case.objects.get(case_number=self.kwargs['case_number'])
        case.scheduling_conference_date = request.POST['scheduling_conference_date']
        case.save(update_fields=['scheduling_conference_date'])
        return HttpResponseRedirect(self.get_success_url())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        return self.kwargs

    def get_success_url(self):
        return reverse('track', kwargs=self.kwargs)


class TrackView(FormView):
    template_name = 'remind/track_form.html'
    form_class = TrackForm

    def get_form_kwargs(self):
        return self.kwargs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TrialView(FormView):
    template_name = 'remind/trial_form.html'
    form_class = TrialForm

    def get_form_kwargs(self):
        return self.kwargs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OrderView(FormView):
    template_name = 'remind/order_form.html'
    form_class = OrderForm

    def get_form_kwargs(self):
        return self.kwargs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)