from django.shortcuts import render

# Create your views here.

def greetings(request):
    return render(request, 'greetings/greetings.html', {})