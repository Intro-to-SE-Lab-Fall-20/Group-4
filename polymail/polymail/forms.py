from django import forms
import datetime

class EmailForm(forms.Form):
        to_email = forms.EmailField(label="To", required=True)
        subject = forms.CharField(label="Subject", max_length=998, required=True)
        cc = forms.CharField(label="cc", max_length=90)
        body = forms.CharField(label="Body", widget=forms.Textarea)
        attachment = forms.Field(label="attachment", widget = forms.FileInput)