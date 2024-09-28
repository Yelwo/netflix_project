from rest_framework import serializers

from . import models

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'


class CreateScreenCotentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    genres = GenreSerializer(many=True)
    type = serializers.ChoiceField([('TV Show', 'TV Show'),('Movie','Movie')], write_only=True)

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        genre_names = [genre['name'] for genre in genres]
        existing_genres = models.Genre.objects.filter(name__in=genre_names)
        existing_genre_names = existing_genres.values_list('name', flat=True)
        genres_to_create = [models.Genre(name=genre) for genre in genre_names if genre not in existing_genre_names]
        created_genres = models.Genre.objects.bulk_create(genres_to_create)
        genres = list(existing_genres) + created_genres

        if (sc_type := validated_data.pop('type')) == 'Movie':
            scree_content, _ = models.Movie.objects.get_or_create(**validated_data)
        if sc_type == 'TV Show':
            scree_content, _ = models.TVShow.objects.get_or_create(**validated_data)
            
        scree_content.genres.set(genres)
        return scree_content

