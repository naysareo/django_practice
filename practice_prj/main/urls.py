from . import views
from django.urls import path, include

urlpatterns = [
    path('index1/', views.IndexMainView.as_view(), name='index'),
    path('index2/', views.register_view, name='index2'),
    path('login/', views.login_view, name='login'),
]