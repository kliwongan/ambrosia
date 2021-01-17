from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('api/ingredient', views.IngredientView.as_view()),
    path('api/food-storage', views.FoodStorageView.as_view()),
    path('api/meal-recipe', views.MealView.as_view()),
    path('api/user-schedule', views.UserScheduleView.as_view()),
    path('api/create-schedule', views.CreateScheduleView.as_view()),
    path('add-item', views.addingredient, name='additem'),
    path('sub-item', views.subingredient, name='subitem'),
    path('storage', views.Storage, name='storage'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('recommend', views.Meal_recommendation, name='reccomend'),
    path('add-meal', views.add_meal, name='add_meal'),
    path('checklist', views.checklist, name='checklist'),
]
