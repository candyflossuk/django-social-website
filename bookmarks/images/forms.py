from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


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

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(
            commit=False
        )  # Create image instance by calling save method of the form
        image_url = self.cleaned_data["url"]  # Get URL
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = (
            f"{name}.{extension}"  # Generate image name combining slug and extension
        )

        # download image from the given url
        response = request.urlopen(image_url)  # Download image
        image.image.save(
            image_name, ContentFile(response.read()), save=False
        )  # Save to the media directory

        if (
            commit
        ):  # Maintain the behaviour of the save method - only committing if commit = True
            image.save()
        return image
