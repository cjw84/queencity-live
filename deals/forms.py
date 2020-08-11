from django import forms
from .models import Company, Deal

#Creates form based on the Company Model
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'overview', 'industry', 'location']
        labels = {
            'location': 'Location (Zoom out to view map, then select location)'
        }

#Creates form based on Deal Model
class DealForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(
        attrs={'type': 'date'}
    ), required=False)

    class Meta:
        model = Deal
        fields = ['company', 'investor', 'funding', 'date', 'funding_amount']
