from django.forms import ModelForm
from django import forms
from .models import Case


class CaseForm(ModelForm):
    class Meta:
        model = Case
        fields = [
            'case_number',
            'prosecutor_name',
            'paralegal_name',
            'supervisor_name',
            'arraignment_date',
        ]


class SchedulingForm(ModelForm):
    class Meta:
        model = Case
        fields = [
            'scheduling_conference_date',
        ]


class TrackForm(ModelForm):
    class Meta:
        model = Case
        fields = [
            'track',
        ]


class TrialForm(ModelForm):
    date = forms.DateTimeField(label='Date', input_formats=['%Y-%m-%d %H:%M'])
