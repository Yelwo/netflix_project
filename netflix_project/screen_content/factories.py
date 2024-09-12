import abc

from . import models


class Content:
    @abc.abstractmethod
    def create_screen_content(self) -> models.ScreenContent:
        # add actors
        return NotImplemented


class TVShowContent(Content):
    def create_screen_content(self) -> models.TVShow:
        # create sezons
        return models.TVShow()


class MovieContent(Content):
    def create_screen_content(self) -> models.Movie:
        return models.Movie()