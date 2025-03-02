from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, JsonResponse

# def hello_world(request):
#     return HttpResponse("Hello, world! This is our interneers-lab Django server.")

def hello_name(request):
    name=request.GET.get("name", "World")
    return JsonResponse({"message": f"Hell0, {name}!"}) 

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', hello_world),
    path('hello/', hello_name),
]
