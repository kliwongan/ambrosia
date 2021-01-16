1. APIView,
  for the api, it can be opened in the following urls:
  /api/meals for meals recipe
  /api/food-storage for food storage (a little bit messy in quantity json)
  /api/ingredient for ingredient list
  
  if you want to add new meals, ingredient, use django admin
  
 2. Django Admin
    create super user using python manage.py createsuperuser then open it in /admin
    there are 5 models inside and the description can be found in models.py
 
 3. User Authentication
    register path can be found in /api/register
    login path can be found in /api/login
    Since the username is already unique, than it can be taken as variable name in Food_Storage model
 
 4. Functions
    Currently I only have 2 functions which is adding Ingredients and removing it, the function can be found in views.py
    In fact, it's still for only adding 1 ingredient and update the quantity, but I've commented the function in case the ingredients is in dictionary form
    For substraction, It also has feature to count how many ingredient needed left.
    For the recipe function, I guess we will add manually using Django-admin just for few 
    
 5. Models
    For the recipe, we can add imagefield for it, or maybe react can storage it somehow (?)
    
 So, what we currently need is the schedule field and storage for input image. I don't really understand how to integrate 2 or more different apps in django and using sharing models and storage. So, maybe one app should be enough and we just add more pages and function inside views.py. 
