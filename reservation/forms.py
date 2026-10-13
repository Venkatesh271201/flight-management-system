from django import forms
from django.contrib.auth.models import User
from .models import Booking

# Booking form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # No additional fields since user and flight are set in view

# User registration form
class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'].strip(),
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )
        return user

# Login form (optional if using Django's built-in auth views)
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
