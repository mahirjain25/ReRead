from django import forms
from proofread.models import Document

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()