from django.urls import path
from . import views

urlpatterns = [
    path('add_country/', views.AddCountryView.as_view(), name='add_country'),
    path('add_manufacturer/', views.AddManufacturerView.as_view(), name='add_manufacturer'),
    path('add_car_engine/', views.AddCarEngineView.as_view(), name='add_car_engine'),
    path('add_car/', views.AddCarView.as_view(), name='add_car'),
    path('car/', views.CarView.as_view(), name='car'),
    path('detail_view/<int:pk>/', views.CarDetailView.as_view(), name='detail_view'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

]