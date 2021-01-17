from rest_framework import serializers
from .models import Meal, Ingredient, Food_Storage, Storageingredient, Mealingredient, Daily_Schedule, User_Schedule
from django.core.serializers.json import DjangoJSONEncoder
import json


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class Food_StorageSerializer(serializers.ModelSerializer):
    Ingredients = serializers.SerializerMethodField('get_ingredients')

    class Meta:
        model = Food_Storage
        fields = '__all__'

    def get_ingredients(self, obj):
        ingredients = obj.Ingredients.all()
        ingredients_list = {}
        for ingredient in ingredients:
            quantity = Storageingredient.objects.get(
                ingredient=ingredient, storage=obj)
            ingredients_list[ingredient.name] = quantity.quantity
        return ingredients_list


class MealSerializer(serializers.ModelSerializer):
    recipe = serializers.SerializerMethodField('get_recipe')

    class Meta:
        model = Meal
        fields = ('name', 'recipe', 'cooking_time', 'description')

    def get_recipe(self, obj):
        ingredients = obj.recipe.all()
        ingredients_list = {}
        for ingredient in ingredients:
            quantity = Mealingredient.objects.get(
                ingredient=ingredient, meal=obj)
            ingredients_list[ingredient.name] = quantity.quantity
        return ingredients_list


class ScheduleSerializer(serializers.ModelSerializer):
    meal = serializers.SerializerMethodField('get_meal')

    class Meta:
        model = Daily_Schedule
        fields = '__all__'

    def get_meal(self, obj):
        return obj.meal.name


class UserScheduleSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(many=True)

    class Meta:
        model = User_Schedule
        fields = '__all__'


class CreateScheduleSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(many=True)

    class Meta:
        model = User_Schedule
        fields = '__all__'
