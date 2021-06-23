from django import forms


class UserInfo(forms.Form):
    text_info = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form input-form',
        'placeholder': 'Enter your text'
    }))


class PasswordForm(forms.Form):
    text_info = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form password-form',
        'placeholder': 'Enter your password'
    }))

