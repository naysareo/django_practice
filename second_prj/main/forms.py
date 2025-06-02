from django import forms
from .models import Book, Author, Genre

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["author", "genres", "title", "text", "image"]


class TestBookForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    genres = forms.ModelChoiceField(queryset=Genre.objects.all())
    title = forms.CharField()
    text = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].choices = [
            (author.id, author.name) for author in Author.objects.all()
        ]
        self.fields['genres'].choices = [
            (genre.id, genre.name) for genre in Genre.objects.all()
        ]


class AuthorForm(forms.Form):
    name = forms.CharField()


class GenresForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]