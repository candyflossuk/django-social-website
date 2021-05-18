from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("title", "url", "description")
        # HiddenInput used to hide this field - as will be sent from JS tool
        widgets = {"url": forms.HiddenInput}
