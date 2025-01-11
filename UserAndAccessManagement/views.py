from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def signin(request):
    if request.method == POST:
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message":"Sign-in Successful","status": "success"})
        else:
            return JsonResponse({"message":"Invalid email or Password", "status":"error"})
    return render(request, "signin.html") # for example