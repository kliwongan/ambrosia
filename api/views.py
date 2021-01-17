from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ingredient, Food_Storage, Storageingredient, User, Meal, Mealingredient, User_Schedule, Daily_Schedule
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import IngredientSerializer, Food_StorageSerializer, MealSerializer, UserScheduleSerializer, CreateScheduleSerializer
from .forms import StorageForm
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


class UserScheduleView(generics.ListAPIView):
    queryset = User_Schedule.objects.all()
    serializer_class = UserScheduleSerializer


class CreateScheduleView(APIView):
    serializer_class = CreateScheduleSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user.username
            meal = serializer.data.get('meal')
            date = serializer.data.get('date')
            new_meal = Meal.objects.get(name=meal)
            new_schedule = Daily_Schedule(date=date, meal=new_meal)
            new_schedule.save()
            user_schedule = User_Schedule(
                user=user, schedule=new_schedule)
            user_schedule.save()

        return Response(UserScheduleSerializer(user_schedule).data, status=status.HTTP_201_CREATED)


def index(request):
    if request.user.is_authenticated:
        return Meal_recommendation(request)
    else:
        return login_view(request)


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
        new_schedule = User_Schedule(user=username)
        new_schedule.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")


def addingredient(request):
    if request.method == 'POST':
        user = request.POST.get('name', False)
        # user = request.user.username

        ingredients = request.POST.get(
            'ingredients', False)  # expect a dictionary
        storage = Food_Storage.objects.filter(user=user)
        if storage.count() == 0:
            new_storage = Food_Storage(user=user)
            new_storage.save()
        storage = Food_Storage.objects.get(user=user)

        # the code when ingredients is in form of dictionary
        # if the input is dictionary

        ''' for ingredient in ingredients.keys():
            check_ingredient = Ingredient.objects.filter(name=ingredient)
            if check_ingredient.count() == 0:
                check_ingredient = Ingredient(name=ingredient)
                check_ingredient.save()
            else:
                check_ingredient = Ingredient.objects.get(name=ingredient)
            add_items = Storageingredient.objects.filter(
                ingredient=check_ingredient, storage=storage)
            # add inputed ingredients
            add_items.quantity += ingredients[ingredient] '''

        # if input is not dictionary, we have quantity as integer variable
        # if quantity is an integer
        quantity = int(request.POST.get('quantity', False))

        check_ingredient = Ingredient.objects.filter(name=ingredients)
        if check_ingredient.count() == 0:
            new_ingredient = Ingredient(name=ingredients)
            new_ingredient.save()
        check_ingredient = Ingredient.objects.get(name=ingredients)
        add_items = Storageingredient.objects.filter(
            ingredient=check_ingredient, storage=storage)
        # add inputed ingredients
        add_items.quantity += quantity

        storage_items = Storageingredient.objects.filter(
            storage=storage).all()
        return render(request, 'app/index.html', {
            'Storage': storage_items
        })
    else:
        return HttpResponseRedirect(reverse('index'))


# storage: object, ingredients: dictionary/string, #quantity: dictionary or variable
def enough_ingredient(storage, ingredients, quantity):
    sub_possible = True
    """check_ingredient = Ingredient.objects.filter(name=ingredients)
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
                sub_possible = False"""

    # for multiple input, quantity is in dictionary
    for ingredient in ingredients:
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
                if add_items.quantity < quantity[ingredient.name]:
                    sub_possible = False

    return sub_possible


def subingredient(request):
    if request.method == 'POST':
        user = request.POST.get('name', False)
        # user = request.user.username

        # if the input is integer
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
                    ingredient_needed[ingredients] = quantity - \
                        add_items.quantity

        # the code when ingredients is in form of dictionary
        """ for ingredient in ingredients:
            check_ingredient = Ingredient.objects.filter(name=ingredient)
            if check_ingredient.count() == 0:
                sub_possible = False
                ingredient_needed[ingredients] = ingredients[ingredient]
            else:
                check_ingredient = Ingredient.objects.get(name=ingredient)
                add_items = Storageingredient.objects.filter(
                    ingredient=check_ingredient, storage=storage)
                if add_items.count() == 0:
                    sub_possible = False
                else:
                    add_items = add_items[0]
                    if add_items.quantity < ingredients[ingredient]:
                        sub_possible = False
                        ingredient_needed[ingredient] = ingredients[ingredient] - add_items.quantity"""

        message = ''
        # sub_possible = enough(storage, ingredients.keys(), ingredients) #when ingreidents is a dictionary
        if sub_possible == True:
            sub_items = Storageingredient.objects.get(
                ingredient=check_ingredient, storage=storage)
            sub_items.quantity -= quantity
            sub_items.save()
        else:
            message = 'Your ingredients is not enough'

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


def Meal_recommendation(request):
    user = request.user.username
    storage = Food_Storage.objects.get(user=user)
    schedules = User_Schedule.objects.get(user=user).schedule.all()
    meals = Meal.objects.all()
    available_meal = []
    non_available_meal = []
    for meal in meals:
        ingredients = meal.recipe.all()
        ingredient_recipe = {}
        for ingredient in ingredients:
            ingredient_obj = Mealingredient.objects.get(
                ingredient=ingredient, meal=meal)
            ingredient_recipe[ingredient.name] = ingredient_obj.quantity
        can_be_made = enough_ingredient(
            storage, ingredients, ingredient_recipe)
        if can_be_made:
            available_meal.append(meal)
        else:
            non_available_meal.append(meal)
    return render(request, 'app/schedule.html', {
        'schedules': schedules,
        'available_meal': available_meal,
        'non_available_meal': non_available_meal
    })


def add_meal(request):
    if request.method == 'POST':
        meal = request.POST.get('meal', False)
        date = request.POST.get('date', False)
        storage = Food_Storage.objects.get(user=request.user.username)
        add_meal = Meal.objects.get(name=meal)
        meal_ingredients = add_meal.recipe.all()
        for ingredient in meal_ingredients:
            user_ingredient = Storageingredient.objects.get(
                storage=storage, ingredient=ingredient)
            meal_recipe = Mealingredient.objects.get(
                meal=add_meal, ingredient=ingredient)
            user_ingredient.quantity -= meal_recipe.quantity
            user_ingredient.save()

        add_schedule = Daily_Schedule(meal=add_meal)
        add_schedule.date = date
        add_schedule.save()
        new_schedule = User_Schedule.objects.get(user=request.user.username)
        new_schedule.schedule.add(add_schedule)
        new_schedule.save()

        return Meal_recommendation(request)
    else:
        return Meal_recommendation(request)


def checklist(request):
    return render(request, 'app/checklist.html', {
        'form': StorageForm()
    })
