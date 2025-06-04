import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views import View
from django.db import transaction
from .models import Car, CustomerUser, Country
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView
from .forms import (AddCountryForm, AddManufacturerForm, AddCarEngineForm, AddCarForm, RegisterForm, LoginForm,
                    AddGroupForm)
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page


# todo Views (CountryView, ManufacturerView, CarEngineView, CarView)


class CountryCreateView(CreateView):
    model = Country
    template_name = 'car/add_country.html'
    fields = ['name']
    success_url = reverse_lazy('car')

    def form_valid(self, form):
        country = form.save(commit=False)
        country.name = country.name + 'gggggggggg'
        country.save()
        return super().form_valid(form)
# class AddCountryView(FormView):
#     template_name = 'car/add_country.html'
#     form_class = AddCountryForm
#     success_url = reverse_lazy('car')
#
#     def form_valid(self, form):
#         try:
#             with transaction.atomic():
#                 country = form.save(commit=False)
#                 country.name = country.name + '2'
#                 country.save()
#                 raise ValueError("Ошибка!")
#         except Exception:
#             print('Произошёл откат')
#         return super().form_valid(form)


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


# class CarView(ListView):
#     model = Car
#     template_name = 'car/car.html'
#     paginate_by = 5
#
#     def get_queryset(self):
#         return Car.objects.select_related('manufacturer', 'engine_model')

def car_view(request):
    object_list = Car.objects.select_related('manufacturer', 'engine_model').all()
    paginator = Paginator(object_list, 3)
    num_page = request.GET.get('page')
    page_obj = paginator.get_page(num_page)
    return render(request, 'car/car.html', {'page_obj': page_obj})


class CarDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = reverse_lazy('car')
    model = Car
    template_name = 'car/detail_view.html'
    context_object_name = 'car'
    permission_required = 'car.change_car'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'add-user' in request.GET:
            user_id = request.session.get('_auth_user_id')
            user = CustomerUser.objects.get(pk=user_id)
            moderators = Group.objects.get(name='Moderators')
            user.groups.add(moderators)
        context = super().get_context_data(object=self.object)
        return self.render_to_response(context)

    def handle_no_permission(self):
        return redirect('/car/')


@cache_page(60)
def car_detail_view(request, pk):
    car = Car.objects.select_related('engine_model', 'manufacturer').get(pk=pk)
    if 'add-user' in request.GET:
        user_id = request.session.get('_auth_user_id')
        print(user_id)
    return render(request, 'car/detail_view.html', {'car': car})


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


class UserLoginView(FormView):
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


class AddGroupView(FormView):
    form_class = AddGroupForm
    template_name = 'car/add_group.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('car')

# @permission_required('car.change_car', login_url='car')
def permission_managing(request):
    # moderators = Group.objects.get(name='Moderators')
    # content_type = ContentType.objects.get_for_model(Car)
    # permission = Permission.objects.filter(codename__in=['add_car', 'change_car', 'delete_car', 'view_car'], content_type=content_type)
    # moderators.permissions.add(*permission)
    permission_cache = cache.get('permission')
    user_cache = cache.get('user')
    # if not permission_cache and not user_cache:
    permission = Permission.objects.all()
    user = CustomerUser.objects.get(pk=request.session.get('_auth_user_id'))
    value = random.randint(1, 9999)
    print(f'Значение: {value}')
    #     cache.set('permission', permission, timeout=60)
    #     cache.set('user', user, timeout=60)
    context = {'permission': permission_cache,
               'user': user_cache,
               'random_value': value}
    return render(request, 'car/permissions_managing.html', context)

class PermissionsViewList(ListView):
    model = ContentType
    template_name = 'car/permissions_managing.html'
    context_object_name = 'permissions'

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(Car)
        return Permission.objects.select_related('content_type').filter(content_type=content_type)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model.__name__
        return context




def logout_view(request):
    logout(request)
    return redirect('/car/')