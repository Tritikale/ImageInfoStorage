from django import forms


class UserInfo(forms.Form):
    text_info = forms.CharField(widget=forms.Textarea)