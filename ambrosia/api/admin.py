from django.contrib import admin
from .models import Ingredient, Food_Storage, Storageingredient, Meal, Mealingredient
# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Food_Storage)
admin.site.register(Storageingredient)
admin.site.register(Meal)
admin.site.register(Mealingredient)
