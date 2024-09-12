from django.urls import path, include

from screen_content.views import MovieViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies', MovieViewset, basename='movies')
urlpatterns = [
    path('', include(router.urls)),
]