from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('book/', views.IndexView.as_view(), name="book"),
    path('author/', views.AuthorCreateView.as_view(), name="author"),
    path('genres/', views.GenresCreateView.as_view(), name="genres"),
    # path('detail_book/<int:pk>', views.DetailViewBook.as_view(), name="detail_view"),
    path('detail_book/<int:pk>', views.detail_view, name="detail_view"),
    path('base/', views.BaseHTML.as_view(), name="base"),
    path('navbar/', views.NavbarHTML.as_view(), name="navbar"),
    path('footer/', views.FooterHTML.as_view(), name="footer"),
    path('home/', views.HomeHTML.as_view(), name="home"),
    path('about/', views.AboutHTML.as_view(), name="about"),
    path('book_update/<int:pk>', views.BookUpdateView.as_view(), name="book_update"),
    path('test_book_form/', views.TestBookView.as_view(), name="test_book_form"),

]