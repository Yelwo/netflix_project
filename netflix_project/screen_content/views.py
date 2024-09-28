from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import views

from . import serializers
from . import models

# Create your views here.

class ScreenCotentViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.ScreenContent.objects.all()
    serializer_class = serializers.CreateScreenCotentSerializer
    permission_classes = []
