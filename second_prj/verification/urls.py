from django.urls import path
from . import views
urlpatterns = [
    path('registration_view/', views.CreateUserView.as_view(), name='registration_view'),
    # path('registration_view/', views.registration, name='registration_view'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
]