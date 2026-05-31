from django import forms
from .models import LoanRecord


class LoanRecordForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    paid_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = LoanRecord
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'sr': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'interest': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'interest_rate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1% or 2%'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5 Month'}),
            'final_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Clear or Partial'}),
        }
