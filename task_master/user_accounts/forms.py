from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from .models import UserProfile  # Импорт модели профиля пользователя


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=50,
                                 widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control Roboto'}))
    last_name = forms.CharField(label='Фамилия', max_length=50,
                                widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control Roboto'}))
    email = forms.EmailField(label='Электронная почта', max_length=100,
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control Roboto'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control Roboto'}))
    password2 = forms.CharField(label='Подтвердите пароль (еще раз)',
                                widget=forms.PasswordInput(attrs={'class': 'form-control Roboto'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control Roboto'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control Roboto'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control Roboto'}),
            'email': forms.EmailInput(attrs={'class': 'form-control Roboto'})
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = ''  # Или любое другое значение, которое не нужно шифровать
        user.first_name = ''
        user.last_name = ''
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email']
            )
        return user


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control Roboto'}))
    password = forms.CharField(label=_("Пароль"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': "current-password", 'class': 'form-control Roboto'}))
