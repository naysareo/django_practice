from django.contrib import admin
from .models import Book, Author, Genre

class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "text", "image", "published")
    list_display_links = ("id", "author")
    search_field = ("id", "author", "title")
    list_filter = ("author", "title")
    list_editable = ("published", )

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
