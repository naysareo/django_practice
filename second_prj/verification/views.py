from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import RegistrationForm, LoginForm
from .forms import UserRegistrationForm, LoginForm
from .models import CustomerUser


def registration(request) -> render:
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/author/')
    else:
        form = RegistrationForm()
    return render(request, 'verification/registration.html', {'form': form})


def login_view(request) -> render:
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print("DEBUG:", username, password)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/genres/')
            else:
                form.add_error(None, "Неверный логин или пароль")
    else:
        form = LoginForm()
    return render(request, 'verification/login.html', {'form': form})


def logout_view(request) -> None:
    logout(request)
    return redirect('/book/')


class CreateUserView(FormView):
    model = CustomerUser
    form_class = UserRegistrationForm
    template_name = 'verification/registration.html'
    success_url = reverse_lazy('book')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
