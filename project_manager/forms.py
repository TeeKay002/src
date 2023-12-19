# project_manager/forms.py
from django import forms
from .models import Project, Update

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'file_upload', 'need_money', 'amount_needed', 'already_paid', 'stages']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'amount_needed': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'style': 'width: 100%', 'type': 'number', 'localize': True}),
            'already_paid': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'style': 'width: 100%', 'type': 'number', 'localize': True}),
        }

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ['status', 'amount_paid', 'description']  # Corrected field name to 'amount_paid'
