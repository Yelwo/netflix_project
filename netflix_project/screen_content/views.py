from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import views
from rest_framework import response

from rest_framework.decorators import action


from . import serializers
from . import models

# Create your views here.

class ScreenCotentViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.ScreenContent.objects.all()
    serializer_class = serializers.CreateScreenCotentSerializer
    permission_classes = []


class UserProfileViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.AddScreenContentToHistorySerializer
    permission_classes = []

    @action(methods=['put'], detail=True)
    def add_to_history(self, request, pk=None):
        serialier = serializers.AddScreenContentToHistorySerializer(instance=request.user.user_profile, data=request.data)
        serialier.is_valid(raise_exception=True)
        serialier.save()
        return response.Response(serialier.data)
