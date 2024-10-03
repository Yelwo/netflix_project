from itertools import zip_longest

import pytest
from django.urls import reverse

from screen_content import serializers
from screen_content import models


@pytest.mark.django_db
class TestScreenContent:
    def test_create(self, client, faker, user_profile):
        data = {
            'title': faker.name(),
            'genres': [{'name': faker.sentence(nb_words=2)} for _ in range(3)],
            'type': 'Movie',
        }

        client.force_login(user_profile.user)
        url = reverse('screen-content-list')
        response = client.post(url, data=data, content_type='application/json')

        
        assert response.status_code == 201
        assert response.data['title'] == data['title']
        for created, genre in zip_longest(response.data['genres'], data['genres']):
            assert created['name'] == genre['name']
    
    def test_genres_are_unique(self, client, faker, user_profile, screen_content_factory, genre):
        screen_content_factory(genres=[genre])
        data = {
            'title': faker.name(),
            'genres': [{'name': genre.name}],
            'type': 'Movie',
        }


        client.force_login(user_profile.user)
        url = reverse('screen-content-list')
        response = client.post(url, data=data, content_type='application/json')

        assert models.Genre.objects.get(name=genre.name)
    
    def test_movie_type(self, client, faker, user_profile, genre):
        data = {
            'title': faker.name(),
            'genres': [{'name': genre.name}],
            'type': 'Movie',
        }

        client.force_login(user_profile.user)
        url = reverse('screen-content-list')
        response = client.post(url, data=data, content_type='application/json')

        assert models.Movie.objects.get(title=data['title'])
    
    def test_tv_show_type(self, client, faker, user_profile, genre):
        data = {
            'title': faker.name(),
            'genres': [{'name': genre.name}],
            'type': 'TV Show',
        }

        client.force_login(user_profile.user)
        url = reverse('screen-content-list')
        response = client.post(url, data=data, content_type='application/json')

        assert models.TVShow.objects.get(title=data['title'])


@pytest.mark.django_db
class TestUserProfile:
    def test_add_to_history(self, client, user_profile, screen_content):
        data = {
            'screen_content': {'title': screen_content.title}
        }

        client.force_login(user_profile.user)
        url = reverse('user-profile-add-to-history', kwargs={'pk': user_profile.pk})
        response = client.put(url, data=data, content_type='application/json')

        assert list(user_profile.history.all()) == [screen_content]

    def test_add_to_history_different_user_profile(self, client, faker, user_profile, user_profile_factory, screen_content):
        data = {
            'screen_content': {'title': screen_content.title}
        }
        different_user_profile = user_profile_factory()

        client.force_login(user_profile.user)
        url = reverse('user-profile-add-to-history', kwargs={'pk': different_user_profile.pk})
        response = client.put(url, data=data, content_type='application/json')

        assert list(different_user_profile.history.all()) == []


    def test_add_to_history_screen_content_doesnt_exist(self, faker, client, user_profile, screen_content):
        data = {
            'screen_content': {'title': faker.name()}
        }

        client.force_login(user_profile.user)
        url = reverse('user-profile-add-to-history', kwargs={'pk': user_profile.pk})
        response = client.put(url, data=data, content_type='application/json')

        assert response.status_code == 400
        assert response.json() == {'screen_content': ['Invalid title, object does not exist']}



