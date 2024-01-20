from django.shortcuts import render, HttpResponse
from .models import Skill, Geography, Demand
import requests
from datetime import datetime, timedelta
import pandas as pd


# Create your views here.
def home(request):
    return render(request, 'home.html')


# def todos(request):
#     items = TodoItem.objects.all()
#     return render(request, 'todos.html', {'todos':items})

def demand(request):
    plots = Demand.objects.all()
    df = pd.read_csv("analytics/salary_by_year_filtered.csv")
    table = df.to_html(classes='table', index=False, justify='left')
    title = "Статистика по годам для выбранной профессии"
    df2 = pd.read_csv("analytics/salaries_by_year.csv")
    table2 = df2.to_html(classes='table', index=False, justify='left')
    title2 = "Статистика по годам"
    return render(request, 'demand.html', {'plots': plots, 'table': table, 'table2': table2, 'title': title,
                                           'title2': title2})


def geography(request):
    plots = Geography.objects.all()
    df = pd.read_csv("analytics/vacancies_by_city_filtered.csv")
    table = df.to_html(classes='table', index=False, justify='left')
    title = "Доля вакансий по городам для выбранной профессии"
    df2 = pd.read_csv("analytics/vacancies_by_city.csv")
    table2 = df2.to_html(classes='table', index=False, justify='left')
    title2 = "Доля вакансий по городам"
    df3 = pd.read_csv("analytics/salaries_by_city.csv")
    table3 = df3.to_html(classes='table', index=False, justify='left')
    title3 = "Зарплаты по городам"
    df4 = pd.read_csv("analytics/salaries_by_city_filtered.csv")
    table4 = df4.to_html(classes='table', index=False, justify='left')
    title4 = "Зарплаты по городам для выбранной профессии"
    return render(request, 'geography.html',
                  {'plots': plots, 'table': table, 'table2': table2, 'table3': table3, 'table4': table4, 'title': title,
                   'title2': title2, 'title3': title3, 'title4': title4})


def skills(request):
    skills = Skill.objects.all()
    df = pd.read_csv("analytics/skills_by_year.csv")
    table = df.to_html(classes='table', index=False, justify='left')
    title = "Навыки по годам"
    df2 = pd.read_csv("analytics/skills_by_year_filtered.csv")
    table2 = df2.to_html(classes='table', index=False, justify='left')
    title2 = "Навыки по годам для выбранной профессии"
    return render(request, 'skills.html', {'skills': skills, 'table': table, 'table2': table2, 'title': title,
                                           'title2': title2})


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
