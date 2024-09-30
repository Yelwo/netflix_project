import factory

from screen_content import models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('email')

    class Meta:
        model = models.User

class UserProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.UserProfile

class GenreFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('sentence', nb_words=2)

    class Meta:
        model = models.Genre

class ScreenContentFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=2)

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.genres.add(*extracted)

    class Meta:
        model = models.ScreenContent