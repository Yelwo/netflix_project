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