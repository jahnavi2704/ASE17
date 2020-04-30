from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Users.models import Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (

            'username',
            'password',
            'confirm_password',
            'email',


        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('password', 'Password Did Not Match')


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (

        'phone_no',
        'address',
        'card_no',
        'display_pic',
        )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (

            'phone_no',
            'address',
            'card_no',
            'display_pic',
        )
