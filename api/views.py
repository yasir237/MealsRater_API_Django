from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import Meal, Rating
from django.contrib.auth.models import User
from .serializers import MealSerializer, RatingSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny, )


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_excepion = True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user = serializer.instance)
        return Response(
            {'token': token.key,},
            status=status.HTTP_201_CREATED,
        )
    
    def list(self, request, *args, **kwargs):
        response = {
            'message': 'you cant creat rating like that'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    



class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
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

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def update(self, request, *args, **kwargs):
        response = {
            'message': "Invalid function to update"
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def create(self, request, *args, **kwargs):
        response = {
            'message': "Invalid function to create"
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
