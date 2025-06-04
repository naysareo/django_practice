from django import forms
from django.contrib.auth.models import Group

from .models import Country, Manufacturer, CarEngine, Car, CustomerUser


# todo FORMS (CountryForm, ManufacturerForm, CarEngineForm, CarForm)


class AddCountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class AddManufacturerForm(forms.ModelForm):
    # country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Choice country")
    class Meta:
        model = Manufacturer
        fields = ['name', 'country']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['country'].empty_label = 'Select Country'


class AddCarEngineForm(forms.ModelForm):
    release_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = CarEngine
        fields = ['name', 'horse_power', 'manufacturer', 'release_date']


class AddCarForm(forms.ModelForm):
    release_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Car
        fields = ['manufacturer', 'car_model', 'engine_model', 'serial_number', 'release_date', 'car_image']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'first_name', 'password', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        print(f"Password1: {password} / Password2: {password2}")
        if password != password2:
            raise forms.ValidationError("Incorrect passwords!")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']