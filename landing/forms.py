from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=70, widget=forms.EmailInput(
        attrs = {
            'class':'mb-4',
            'placeholder' : 'Enter a valid email',
            'required' : True,
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'placeholder': 'Password',
            'required' : True
        }
    ))

class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username','email','first_name','last_name')

        widgets = {
            'username' : forms.TextInput(
                attrs={
                    'class':'mb-4',
                    'placeholder': 'username'
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    'class':'mb-4',
                    'placeholder':'Enter a valid email'
                }
            ),
            'first_name' : forms.TextInput(
                attrs={
                    'class':'mb-4',
                    'placeholder':'First Name'
                }
            ),
            'last_name' : forms.TextInput(
                attrs={
                    'class':'mb-4',
                    'placeholder' : 'Last Name'
                }
            )
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password doesn't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email','username','first_name','last_name','is_admin','is_active')

    def clean_password(self):
        return self.initial['password']