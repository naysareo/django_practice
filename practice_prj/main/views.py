from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .models import Main
from .forms import RegisterForm, LoginForm
from django.contrib import messages

def index(request):
    context = {}
    if request.user.is_authenticated:
        context['greeting'] = f"Привет, {request.user.email}"
    else:
        context['greeting'] = "Вы не авторизованы"
    session = request.session
    for a, b in session.items():
        print(f"{a}: {b}")
    return render(request, "main/index.html", context)


class IndexMainView(ListView):
    model = Main
    template_name = "main/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session
        context["greeting"] = "Hello"
        return context





def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/index1/")
    return render(request, "main/index2.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/index1/")
            else:
                messages.error(request, 'Неверный email или пароль')
    return render(request, 'main/login.html', {"form": form})