from django.urls import path, include

from screen_content.views import ScreenCotentViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'screen-content', ScreenCotentViewset, basename='screen-content')
urlpatterns = [
    path('', include(router.urls)),
]