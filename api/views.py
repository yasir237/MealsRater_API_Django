from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Meal, Rating
from django.contrib.auth.models import User
from .serializers import MealSerializer, RatingSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def rate_meal(self, request, pk=None):
        if 'stars' not in request.data:
            return Response({'message': 'Stars not provided in request'}, status=status.HTTP_400_BAD_REQUEST)

        meal = Meal.objects.get(pk=pk)
        stars = request.data['stars']
        user = request.user  # güvenli şekilde giriş yapan kullanıcı

        rating, created = Rating.objects.update_or_create(
            meal=meal,
            user=user,
            defaults={'stars': stars}
        )

        serializer = RatingSerializer(rating)
        return Response({
            'message': 'Meal rate created' if created else 'Meal rate updated',
            'result': serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
