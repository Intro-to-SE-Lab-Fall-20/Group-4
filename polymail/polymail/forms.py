from django import forms
import datetime

class EmailForm(forms.Form):
        to_email = forms.EmailField(label="To", required=True)
        subject = forms.CharField(label="Subject", max_length=998, required=True)
        cc = forms.CharField(label="cc", max_length=90, required=False)
        body = forms.CharField(label="Body", widget=forms.Textarea)
        # attachment = forms.Field(label="attachment", widget=forms.FileInput, required=False)
        attachment = forms.CharField(label="attachment", max_length=1000, required=False)

class SearchForm(forms.Form):
        search_query = forms.CharField(label="Enter Search Term")

class NotesForm(forms.Form):
        title = forms.CharField(label="Title", required=True)
        