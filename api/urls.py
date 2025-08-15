from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import MealViewSet, RatingViewSet


router = routers.DefaultRouter()
router.register('meals', MealViewSet)
router.register('rating', RatingViewSet)


urlpatterns = [
    path('', include(router.urls))
]
