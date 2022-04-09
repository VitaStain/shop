from django import forms
from django.core.exceptions import ValidationError

from main.models import Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(str(phone)) != 12 or str(phone)[:3] != '375':
            raise ValidationError('Номер должен быть равен 12 символов и в формате 375**')
        return phone


class UserEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'phone', 'address', 'send_message')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(str(phone)) != 12 or str(phone)[:3] != '375':
            raise ValidationError('Номер должен быть равен 12 символов и в формате 375**')
        return phone
