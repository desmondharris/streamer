from django.db import models
from django.contrib.auth.models import User



class WatchedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    poster = models.CharField(max_length=255)
    def __str__(self):
        return f"user: {self.user.username}, title: {self.title}, year: {self.year}, poster: {self.poster}, imdb_id: {self.imdb_id}"


class WatchedTV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=255, unique=True)
    season = models.IntegerField()
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    poster = models.CharField(max_length=255)
    def __str__(self):
        return f"user: {self.user.username}, title: {self.title}, year: {self.year}, poster: {self.poster}, imdb_id: {self.imdb_id}, season: {self.season}"
# Create your models here.
