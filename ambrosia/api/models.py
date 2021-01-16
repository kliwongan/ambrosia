from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    pass


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    special_item = models.CharField(max_length=64, default="No")

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
    Cooking_time = models.TimeField(default=None)


class Mealingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
