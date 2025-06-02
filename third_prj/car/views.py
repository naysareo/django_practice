from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.views import View

from .models import Car, CustomerUser
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView
from .forms import AddCountryForm, AddManufacturerForm, AddCarEngineForm, AddCarForm, RegisterForm, LoginForm


# todo Views (CountryView, ManufacturerView, CarEngineView, CarView)

class AddCountryView(FormView):
    template_name = 'car/add_country.html'
    form_class = AddCountryForm
    success_url = reverse_lazy('car')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddManufacturerView(FormView):
    template_name = 'car/add_manufacturer.html'
    form_class = AddManufacturerForm
    success_url = reverse_lazy('car')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddCarEngineView(FormView):
    template_name = 'car/add_engine.html'
    form_class = AddCarEngineForm
    success_url = reverse_lazy('car')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddCarView(FormView):
    template_name = 'car/add_car.html'
    form_class = AddCarForm
    success_url = reverse_lazy('car')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CarView(ListView):
    model = Car
    template_name = 'car/car.html'

    def get_queryset(self):
        return Car.objects.select_related('manufacturer', 'engine_model')


class CarDetailView(DetailView):
    model = Car
    template_name = 'car/detail_view.html'
    context_object_name = 'car'


class RegisterView(FormView):
    template_name = 'car/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('car')

    def form_valid(self, form):
        if 'super-user-btn' in self.request.POST:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = CustomerUser.objects.create_superuser(email, password)
            print("Superuser user successfully created!")
        else:
            user = form.save()
            print("Regular user successfully created!")
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'car/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('car')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)
        print(user)
        login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/car/')