from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, JsonResponse
import re

def special_char(s):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    return bool(regex.search(s))

# def hello_world(request):
#     return HttpResponse("Hello, world! This is our interneers-lab Django server.")

def hello_name(request):
    # Get 'name' and 'age' from the query string
    name=request.GET.get("name", "World")
    age=request.GET.get("age", None)
    if special_char(name):
        return JsonResponse({"error": "Invalid name. Name can't contain special characters"})
    if not age:
        return JsonResponse({"message": f"Hell0, {name}! Your age is unknown"}) 
    elif int(age)<0:
        return JsonResponse({"error": "Invalid age. Age can't be -ve"})
    
    return JsonResponse({"message": f"Hell0, {name}! Your age is {age}"}) 

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', hello_world),
    path('hello/', hello_name),
]
