from rest_framework import serializers
from .models import Meal, Ingredient, Food_Storage, Storageingredient
from django.core.serializers.json import DjangoJSONEncoder


class StorageIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storageingredient
        fields = ('quantity',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'special_item')


class IngredientSerializer2(serializers.ModelSerializer):
    quantity = StorageIngredientSerializer(many=True)

    class Meta:
        model = Ingredient
        fields = ('name', 'special_item', 'quantity')


class Food_StorageSerializer(serializers.ModelSerializer):
    Ingredients = IngredientSerializer2(many=True)

    class Meta:
        model = Food_Storage
        fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('name', 'recipe', 'cooking_time')
