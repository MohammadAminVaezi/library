from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    nationality = models.CharField(max_length=200, default=None)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, related_name="books")
    genre = models.CharField(max_length=100)
    ratings = models.ManyToManyField(User, blank=True, through='Comment')
    rate = models.FloatField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    cover = models.ImageField(
        upload_to='library/static/covers/', default='static/covers/default-cover.jpeg')
    view_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.SmallIntegerField(
        choices=[(i, i) for i in range(1, 6)], null=True, blank=True)

    class Meta:
        unique_together = (
            'book',
            'user'
        )
