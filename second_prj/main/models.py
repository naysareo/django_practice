import logging

from django.db import models
from django.utils import timezone
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=90)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"(name={self.name})"


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"(genre={self.name})"


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books", null=True, blank=True, verbose_name="Author")
    genres = models.ManyToManyField(Genre)
    title = models.CharField(max_length=50)
    text = models.CharField()
    image = models.ImageField(upload_to="main/")
    published = models.DateTimeField(default=timezone.now())


    def save(self, *args, **kwargs):
        logging.info("Сохраняется книга!")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_update', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"(title={self.title}, text={self.text})"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Book"
        ordering = ['-published']