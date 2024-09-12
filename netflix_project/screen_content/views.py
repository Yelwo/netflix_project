from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins

from . import serializers
from . import models

# Create your views here.

class MovieViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer
    permission_classes = []
