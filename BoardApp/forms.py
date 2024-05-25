from django import forms
from django.core.exceptions import ValidationError

from .models import Ad, UserResponse


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'text',]
        widgets = {'author': forms.HiddenInput()}


class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['text',]
        widgets = {'author': forms.HiddenInput()}


class UserResponseAcceptForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = []
        widgets = {'author': forms.HiddenInput()}
