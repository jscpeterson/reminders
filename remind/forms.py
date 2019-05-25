from material.forms import ModelForm
from .models import Case


class CaseForm(ModelForm):
    class Meta:
        model = Case
        fields = '__all__'

