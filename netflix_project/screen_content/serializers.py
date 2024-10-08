import random
import string

from rest_framework import serializers
from rest_framework import fields

from . import models

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'


class ScreenContentSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = models.ScreenContent
        fields = '__all__'


class CreateScreenCotentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=60)
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
            screen_content, _ = models.Movie.objects.get_or_create(**validated_data)
        if sc_type == 'TV Show':
            screen_content, _ = models.TVShow.objects.get_or_create(**validated_data)

        screen_content.genres.set(genres)
        return screen_content


class AddScreenContentToHistorySerializer(serializers.Serializer):
    screen_content = ScreenContentSerializer(write_only=True)

    def update(self, instance, validated_data):
        instance.history.add(validated_data['screen_content'])
        return instance

    def validate(self, attrs):
        try:
            attrs['screen_content'] = models.ScreenContent.objects.get(**attrs['screen_content'])
        except models.ScreenContent.DoesNotExist:
            raise serializers.ValidationError({'screen_content': ['Invalid title, object does not exist']})
        return attrs


class CurrentUserProfileDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.user_profile


class RatingSerializer(serializers.ModelSerializer):
    user_profile = serializers.HiddenField(default=CurrentUserProfileDefault())
    content = serializers.PrimaryKeyRelatedField(queryset=models.ScreenContent.objects.all())

    class Meta:
        model = models.Rating
        fields = ['content', 'rate', 'user_profile']


class CreationIntegerField(fields.IntegerField):
    def to_representation(self, value):
        return super().to_representation(value.pk)


class BulkRatingSerializer(serializers.ModelSerializer):
    content = CreateScreenCotentSerializer()
    user_profile = CreationIntegerField()

    def create(self, validated_data):
        content = CreateScreenCotentSerializer(data=validated_data.pop('content'))
        content.is_valid()
        content.save()
        try:
            user_profile = models.UserProfile.objects.get(pk=validated_data['user_profile'])
        except models.UserProfile.DoesNotExist:
            user = models.User.objects.create(username=''.join(random.choices(string.ascii_letters, k=8)))
            user_profile = models.UserProfile.objects.create(pk=validated_data['user_profile'], user=user)

        rating, _ = models.Rating.objects.get_or_create(rate=validated_data['rate'], user_profile=user_profile, content=content.instance)
        return rating

    class Meta:
        model = models.Rating
        fields = ['content', 'rate', 'user_profile']