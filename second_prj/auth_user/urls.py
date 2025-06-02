from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.UserLoginView.as_view(), name='login'),
    # path('logout/', views.UserLogoutPage.as_view(), name='logout'),
    # path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    # path('update_profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('2register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)