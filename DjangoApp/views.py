from django.shortcuts import render, HttpResponse
from .models import TodoItem
import requests
from datetime import datetime, timedelta
# Create your views here.
def home(request):
    return render(request, 'home.html')

def todos(request):
    items = TodoItem.objects.all()
    return render(request, 'todos.html', {'todos':items})

def demand(request):
    return render(request, 'demand.html')

def geography(request):
    return render(request, 'geography.html')

def skills(request):
    return render(request, 'skills.html')

def last_vacancies(request):
    now = datetime.now()

    past_24_hours = now - timedelta(hours=24)

    past_24_hours_str = past_24_hours.strftime('%Y-%m-%dT%H:%M:%S')

    response = requests.get('https://api.hh.ru/vacancies', params={
        'text': 'Gamedev',
        'date_from': past_24_hours_str,
        'per_page': 10,
        'order_by': 'publication_time'
    })

    vacancies = response.json()['items']

    return render(request, 'LastVacancies.html', {'vacancies': vacancies})

