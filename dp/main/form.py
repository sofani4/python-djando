from django import forms
from .models import Costs, Income


class DateInput(forms.DateInput):
    input_type = 'date'


class CostsForm(forms.ModelForm):
    class Meta:
        model = Costs
        fields = '__all__'
        widgets = {'author': forms.HiddenInput,
                   'created_at': DateInput(),}


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        widgets = {'author': forms.HiddenInput,
                   'created_at': DateInput(), }


class DataFilterForm(forms.Form):
    start_date = forms.DateField(label='Начальная дата', widget=DateInput())
    end_date = forms.DateField(label='Конечная дата', widget=DateInput())