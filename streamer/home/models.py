from django.db import models
from django.contrib.auth.models import User


class UserVideo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255)
    is_movie = models.BooleanField(default=True)
    season = models.IntegerField(null=True, blank=True)
    episode = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} is watching {self.video_id}"


class InProgressMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=255)
    current_time = models.FloatField(default=0.0)
    def __str__(self):
        return f"{self.user.username} is watching {self.video_id}"


class WatchedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user.username} watched {self.video_id}"


class InProgressTV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=255)
    current_time = models.FloatField(default=0.0)
    season = models.IntegerField()
    episode = models.IntegerField()
    def __str__(self):
        return f"{self.user.username} is watching {self.video_id}"
# Create your models here.
