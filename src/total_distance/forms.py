from django import forms


class RequestForm(forms.Form):
    request_id = forms.CharField(max_length=50)  # TODO add validation
    coordinates = forms.CharField(widget=forms.Textarea)  # TODO add validation
