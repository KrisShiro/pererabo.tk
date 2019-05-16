from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


from .models import Place

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Username')
    password = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
                               label='Password')


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=200, help_text='Required')
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=200, help_text='Required')
    last_name = forms.CharField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'E-mail'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Имя'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Фамилия'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Повторите пароль'})


class MyUserChangeForm(UserChangeForm):
    username = forms.CharField(max_length=200, help_text='Required')
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=200, help_text='Required')
    last_name = forms.CharField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Имя пользователя', 'value': user.username})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'E-mail', 'value': user.email})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Имя', 'value': user.first_name})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Фамилия', 'value': user.last_name})


class AddPlaceForm(forms.ModelForm):
    address = forms.CharField(max_length=100)
    coordinate_x = forms.FloatField()
    coordinate_y = forms.FloatField()
    plastic = forms.BooleanField(required=False)
    paper = forms.BooleanField(required=False)
    glass = forms.BooleanField(required=False)
    accum = forms.BooleanField(required=False)

    class Meta:
        model = Place
        fields = ('address', 'coordinate_x', 'coordinate_y')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Адрес'})
        self.fields['coordinate_x'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'X'})
        self.fields['coordinate_y'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Y'})
        self.fields['plastic'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['paper'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['glass'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['accum'].widget.attrs.update(
            {'class': 'form-control'})


















