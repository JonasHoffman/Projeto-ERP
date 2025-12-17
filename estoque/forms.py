from django import forms
from django.forms import inlineformset_factory



class UploadNFeForm(forms.Form):
    xml_file = forms.FileField(label='Envie o arquivo XML')