from django.urls import path, include

from screen_content import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'screen-content', views.ScreenCotentViewset, basename='screen-content')
router.register(r'user-profile', views.UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('', include(router.urls)),
]