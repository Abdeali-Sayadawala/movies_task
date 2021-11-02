from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Movies(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    released_year = models.CharField(max_length=4, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    movie_id = models.CharField(max_length=255, null=True, blank=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title