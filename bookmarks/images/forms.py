from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("title", "url", "description")
        # HiddenInput used to hide this field - as will be sent from JS tool
        widgets = {"url": forms.HiddenInput}

    def clean_url(self):
        """
        - Get value of the url field by accessing the cleaned_data dict of the form instance
        - Split the URL to get the file extension and check whether it is one of the valid extensions.
        """
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not match valid image extensions"
            )
        return url
