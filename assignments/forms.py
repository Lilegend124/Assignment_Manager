import datetime

from .models import Class_Item, User, Document
from django.forms import ModelForm
from django import forms

# class CreateClass(ModelForm):
#   start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
#   end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
  # Username = forms.CharField(max_length=100)
  # class Meta:
  #   model = Class_Item
  #   fields = ["class_title","meeting_days", "Username"]


class DateInput(forms.DateInput):
    input_type = 'date'

from django.forms.widgets import SelectDateWidget
class DateForm(forms.Form):
    date = forms.DateField(widget=SelectDateWidget())


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'doc', 'class_item', 'author']
