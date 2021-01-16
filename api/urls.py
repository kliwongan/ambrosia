from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('ingredient', views.IngredientView.as_view()),
    path('food-storage', views.FoodStorageView.as_view()),
    path('meal-recipe', views.MealView.as_view()),
    path('add-item', views.addingredient, name='additem'),
    path('sub-item', views.subingredient, name='subitem'),
    path('storage', views.Storage, name='storage'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout')
]
