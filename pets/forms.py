from django import forms
from .models import Pet, Vaccination


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'date_of_birth', 'photo', 'description']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
            }),
        }

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['vaccine_name', 'date_given', 'next_due_date', 'notes']
        widgets = {
            'date_given': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'next_due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Additional notes...'
            }),
        }