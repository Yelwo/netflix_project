import abc

from django.db import models

# Create your models here.

class ScreenContent(models.Model):
    title = models.CharField(max_length=30)

    @abc.abstractmethod
    def rate():
        return NotImplemented
    
    class Meta:
        abstract = True


class Content:
    @abc.abstractmethod
    def create_screen_content(self) -> ScreenContent:
        return NotImplemented


class Movie(ScreenContent, models.Model):
    pass


class TVShow(ScreenContent, models.Model):
    pass


class TVShowContent(Content):
    def create_screen_content(self) -> TVShow:
        return TVShow()


class MovieContent(Content):
    def create_screen_content(self) -> Movie:
        return Movie()
