from django import forms
from django.core.exceptions import ValidationError

from .models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'text',]
        widgets = {'author': forms.HiddenInput()}
