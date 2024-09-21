from rest_framework import serializers

from . import models

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        genres = [models.Genre.objects.get_or_create(genre)[0] for genre in validated_data.pop('genres')]
        movie, _ = models.Movie.objects.get_or_create(**validated_data)
        movie.genres.set(genres)
        return movie

    class Meta:
        model = models.Movie
        fields = '__all__'