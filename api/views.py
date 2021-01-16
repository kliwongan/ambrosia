from django.shortcuts import render
from rest_framework import generics, status
from .serializers import IngredientSerializer, Food_StorageSerializer, MealSerializer, StorageIngredientSerializer
from .models import Ingredient, Food_Storage, Storageingredient, User, Meal, Mealingredient
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

# Create your views here.


class IngredientView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class FoodStorageView(generics.ListAPIView):
    storages = Food_Storage.objects.all()
    queryset = storages
    serializer_class = Food_StorageSerializer


class MealView(generics.ListAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


def index(request):
    return render(request, 'app/index.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        new_storage = Food_Storage(user=username)
        new_storage.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")


def addingredient(request):
    if request.method == 'POST':
        user = request.POST.get('name', False)
        # user = request.user.username
        quantity = int(request.POST.get('quantity', False))
        ingredients = request.POST.get(
            'ingredients', False)  # expect a dictionary
        storage = Food_Storage.objects.filter(user=user)
        if storage.count() == 0:
            new_storage = Food_Storage(user=user)
            new_storage.save()
        storage = Food_Storage.objects.get(user=user)

        # the code when ingredients is in form of dictionary
        """ for ingredient in ingredients.keys():
            check_ingredient = Ingredient.objects.filter(name=ingredient)
            if check_ingredient.count() == 0:
                new_ingredient = Ingredient(name=ingredient)
                new_ingredient.save()
            check_ingredient = Ingredient.objects.get(name=ingredient)
            if add_items.count() == 0:
                add_items = Storageingredient(
                    ingredient=check_ingredient, storage=storage, quantity=quantity)
            else:
                add_items = add_items[0]
                add_items.quantity += quantity
            add_items.save()"""

        check_ingredient = Ingredient.objects.filter(name=ingredients)
        if check_ingredient.count() == 0:
            new_ingredient = Ingredient(name=ingredients)
            new_ingredient.save()
        check_ingredient = Ingredient.objects.get(name=ingredients)

        add_items = Storageingredient.objects.filter(
            ingredient=check_ingredient, storage=storage)
        if add_items.count() == 0:
            add_items = Storageingredient(
                ingredient=check_ingredient, storage=storage, quantity=quantity)
        else:
            add_items = add_items[0]
            add_items.quantity += quantity
        add_items.save()

        storage_items = Storageingredient.objects.filter(
            storage=storage).all()
        return render(request, 'app/index.html', {
            'Storage': storage_items
        })
    else:
        return HttpResponseRedirect(reverse('index'))


# storage: object, ingredients: dictionary/string, #quantity: dictionary
def enough_ingredient(storage, ingredients, quantity):
    sub_possible = True
    check_ingredient = Ingredient.objects.filter(name=ingredients)
    if check_ingredient.count() == 0:
        sub_possible = False
    else:
        check_ingredient = Ingredient.objects.get(name=ingredients)
        add_items = Storageingredient.objects.filter(
            ingredient=check_ingredient, storage=storage)
        if add_items.count() == 0:
            sub_possible = False
        else:
            add_items = add_items[0]
            if add_items.quantity < quantity:
                sub_possible = False

    # for multiple input
    """ for ingredient in ingredients.keys(): 
           check_ingredient = Ingredient.objects.filter(name=ingredient)
            if check_ingredient.count() == 0:
                sub_possible = False
            else:
                check_ingredient = Ingredient.objects.get(name=ingredient)
                add_items = Storageingredient.objects.filter(
                    ingredient=check_ingredient, storage=storage)
                if add_items.count() == 0:
                    sub_possible = False
                else:
                    add_items = add_items[0]
                    if add_items.quantity < quantity[ingredient]:
                        sub_possible = False """

    return sub_possible


def subingredient(request):
    if request.method == 'POST':
        user = request.POST.get('name', False)
        # user = request.user.username
        quantity = int(request.POST.get('quantity', False))
        sub_possible = True
        ingredients = request.POST.get(
            'ingredients', False)  # expect a dictionary
        storage = Food_Storage.objects.get(user=user)
        ingredient_needed = {}

        check_ingredient = Ingredient.objects.filter(name=ingredients)
        if check_ingredient.count() == 0:
            sub_possible = False
            ingredient_needed[ingredients] = quantity
        else:
            check_ingredient = Ingredient.objects.get(name=ingredients)
            add_items = Storageingredient.objects.filter(
                ingredient=check_ingredient, storage=storage)
            if add_items.count() == 0:
                sub_possible = False
            else:
                add_items = add_items[0]
                if add_items.quantity < quantity:
                    sub_possible = False

        # the code when ingredients is in form of dictionary
        """ for 
                ingredient_needed[ingredient] = quantity - add_items.quantity"""

        message = ''
        sub_possible = enough_ingredient(storage, ingredients, quantity)
        if sub_possible == True:
            add_items = Storageingredient.objects.get(
                ingredient=check_ingredient, storage=storage)
            add_items.quantity -= quantity
            add_items.save()
        else:
            message = 'Your ingridients is not enough'

        storage_items = Storageingredient.objects.filter(
            storage=storage).all()
        return render(request, 'app/index.html', {
            'message': message,
            'ingredient_needed': ingredient_needed,
            'Storage': storage_items,
        })
    else:
        return HttpResponseRedirect(reverse('index'))


def Storage(request):
    if request.method == 'POST':
        user = request.POST.get('name', False)
        storage = Food_Storage.objects.get(user=user)
        storage_items = Storageingredient.objects.filter(storage=storage).all()
        return render(request, 'app/index.html', {
            'Storage': storage_items
        })
