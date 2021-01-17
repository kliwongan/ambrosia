from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import datetime


class User(AbstractUser):
    pass


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    eatable_food = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Food_Storage(models.Model):
    user = models.CharField(max_length=64)
    Ingredients = models.ManyToManyField(
        Ingredient, default=None, related_name='Users', through='Storageingredient')

    def __str__(self):
        return f'Storage by {self.user} with {self.Ingredients}'


class Storageingredient(models.Model):
    storage = models.ForeignKey(
        Food_Storage, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='quantity')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.quantity}x {self.ingredient}'


class Meal(models.Model):
    name = models.CharField(max_length=64)
    recipe = models.ManyToManyField(
        Ingredient, default=None, related_name='recipes', through='Mealingredient')
    cooking_time = models.IntegerField(default=0)
    description = models.TextField(default='')

    def __str__(self):
        return f'Meal: {self.name}'


class Mealingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='quantity2')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.meal} need {self.quantity}x {self.ingredient}'


class Daily_Schedule(models.Model):
    date = models.DateField(default=datetime.datetime.now)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.meal.name} scheduled for {self.date}'


class User_Schedule(models.Model):
    user = models.CharField(max_length=64)
    schedule = models.ManyToManyField(Daily_Schedule, default=None)

    def __str__(self):
        return f'user {self.user} schedule'
