from django import forms
from allauth.account.forms import SignupForm
import re


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    tel = forms.CharField(max_length=30, label='telephone', required=False)


class SignupUserForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    tel = forms.CharField(max_length=30, label='telephone', required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise forms.ValidationError('Enter a valid email')
        return email
    
    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        pattern = re.compile(r'^\d+$')
        if not pattern.match(tel):
            raise forms.ValidationError('Enter a valid number')
        return tel

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password does not match')
        return password2


    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.tel = self.cleaned_data['tel']
        user.save()
        return user
