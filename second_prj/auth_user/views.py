from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import RegistrationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User

# class RegisterView(CreateView):
#     template_name = 'auth_user/register.html'
#     form_class = UserRegistration
#
#     def get_success_url(self):
#         return reverse('book')
#
#     def form_valid(self, form):
#         self.object = form.save()
#         login(self.request, self.object)
#         return super().form_valid(form)
#
#
# class UserLoginView(LoginView):
#     template_name = 'auth_user/login.html'
#     redirect_authenticated_user = False
#
#
# class UserLogoutPage(LogoutView):
#     next_page = 'login'
#
#
# class ProfileView(LoginRequiredMixin, DetailView):
#     model = User
#     template_name = 'auth_user/profile_view.html'
#     context_object_name = 'user_obj'
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#
# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = User
#     fields = ['username', 'email']
#     template_name = 'auth_user/profile_edit.html'
#     success_url = reverse_lazy('profile')
#     context_object_name = 'user_obj_update'


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/book/')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    print(request.session)
    return render(request, 'auth_user/2register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/author/')
