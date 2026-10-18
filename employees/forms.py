from django import forms
from .models import employee

class employeeform(forms.ModelForm):
    class Meta:
        model = employee
        fields = '__all__'
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'})
        }