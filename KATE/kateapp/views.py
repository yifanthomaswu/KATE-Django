from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from .models import People, Classes

def index(request):
    return render(request, 'kateapp/home.html')

def personal_page(request):
    login = "md3414"
    person = get_object_or_404(People, login=login)
    context = {
        'name' : person.firstname + " " + person.lastname,
        'person' : person,
    }
    return render(request, 'kateapp/personal_page.html', context)