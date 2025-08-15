from rest_framework import serializers
from .models import Meal, Rating

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'title', 'description',) # id'yi göstermek çok yanlış ama geçici olarak gösteriyoruz. uuid kullanarak yapılır

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'stars', 'user', 'meal')