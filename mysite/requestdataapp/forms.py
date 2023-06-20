from django import forms
from django.core.exceptions import  ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserBioForm(forms.Form):
    name = forms.CharField(max_length=150)
    age = forms.IntegerField(label="Your age", min_value=1, max_value=120)
    bio = forms.CharField(label="Biography", widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and "virus" in file.name:
        raise ValidationError("Error. File name should not contain 'virus'")

def validate_file_size(file: InMemoryUploadedFile) -> None:
    if file.size and file.size > 1000:
        raise ValidationError("Error. File size should be less than 1 Mb.")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name, validate_file_size])