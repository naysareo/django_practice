from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('add_country/', views.CountryCreateView.as_view(), name='add_country'),
    path('add_manufacturer/', views.AddManufacturerView.as_view(), name='add_manufacturer'),
    path('add_car_engine/', views.AddCarEngineView.as_view(), name='add_car_engine'),
    path('add_car/', views.AddCarView.as_view(), name='add_car'),
    path('car/', views.car_view, name='car'),
    path('detail_view/<int:pk>/', views.car_detail_view, name='detail_view'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(template_name='car/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_group/', views.AddGroupView.as_view(), name='add_group'),
    path('permissions/', views.permission_managing, name='permissions'),

]