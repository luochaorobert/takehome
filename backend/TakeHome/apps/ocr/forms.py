from django import forms

from .models import ImageFile


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ["image"]
