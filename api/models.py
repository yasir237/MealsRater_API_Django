from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Genelde uuid kullanırız ancak burada kullanmayacağız
class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)


    # Bu öğenin değerlendirme sayısını döndürür
    def no_of_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        return len(ratings)
    

    def avg_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        total = sum(r.stars for r in ratings)
        avg = total / len(ratings) if ratings else 0
        return avg

    def __str__(self):
        return self.title
    

class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.meal.title
    

    # Her bir kullanıcı bir öğe için sadece bir değerlendirme yapabilir
    unique_together = (('user', 'meal'),)
    index_together = (('user', 'meal'),)