import abc

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


from polymorphic.models import PolymorphicModel

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name
        

class ScreenContent(PolymorphicModel):
    title = models.CharField(max_length=60)
    genres = models.ManyToManyField(Genre, verbose_name="content")
    
    def __str__(self) -> str:
        return self.title


class Movie(ScreenContent):
    pass


class TVShow(ScreenContent):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    history = models.ManyToManyField(ScreenContent, blank=True)

    def __str__(self) -> str:
        return self.user.username


class Rating(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.ForeignKey(ScreenContent, on_delete=models.CASCADE)
    rate = models.FloatField(null=False, validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])

    def __str__(self) -> str:
        return f"{self.user_profile} - {self.content} ({self.rate})"

    class Meta:
        unique_together = ('user_profile', 'content')