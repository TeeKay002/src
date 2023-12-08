from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

    
@login_required
def homePage(request):
    greeting = request.user.username
    return render(request, 'greetings/homePage.html', {'greeting':greeting})


def loginPage(request):
    if request.method == 'POST':
        userName = request.POST.get('userName')
        password = request.POST.get('password')

        user = authenticate(request, username = userName, password = password)

        if user is not None:
            login(request,user)
            return redirect('homePage')
        else:
            return HttpResponse('Error login')
    
    return render(request, 'greetings/loginpage.html', {})


def register(request):
    if request.method== 'POST':
        userName = request.POST.get('userName')
        password = request.POST.get('password')

        new_user = User.object.Create_user(userName, password )
        new_user.save()
        return redirect('homePage')
    
    return render(request, 'greetings/register.html', {})