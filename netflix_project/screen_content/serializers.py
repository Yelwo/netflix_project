from rest_framework import serializers

from . import models

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        genre_names = [genre['name'] for genre in genres]
        existing_genres = models.Genre.objects.filter(name__in=genre_names)
        existing_genre_names = existing_genres.values_list('name')
        genres_to_create = [models.Genre(name=genre) for genre in genre_names if genre not in existing_genre_names]
        created_genres = models.Genre.objects.bulk_create(genres_to_create)
        genres = list(existing_genres) + created_genres

        movie, _ = models.Movie.objects.get_or_create(**validated_data)
        movie.genres.set(genres)
        return movie

    class Meta:
        model = models.Movie
        fields = '__all__'