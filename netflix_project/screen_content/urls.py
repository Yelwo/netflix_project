from django.urls import path, include

from screen_content import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'screen-content', views.ScreenCotentViewset, basename='screen-content')
router.register(r'user-profile', views.UserProfileViewSet, basename='user-profile')
router.register(r'ratings', views.RatingViewSet, basename='ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('ratings/bulk-create/', views.BulkCreateRatings.as_view())
]