from django import forms

def EmailForm(forms.Form):
        to_email = forms.CharField(max_length=320, required=True)
        subject = forms.CharField(max_length=998, required=True)
        cc = forms.CharField(max_length=90)
        message = forms.CharField(widget=forms.Textarea)