from django.shortcuts import render, HttpResponse
from .models import Image, DataTable
import requests
from datetime import datetime, timedelta
import pandas as pd
import io


# Create your views here.
def home(request):
    return render(request, 'home.html')


def demand(request):
    plots = Image.objects.filter(category=Image.Category.DEMAND)
    tables = DataTable.objects.filter(category=DataTable.Category.DEMAND)
    if not tables:
        manual_tables = [
            {"title": "Статистика по годам для разработчика игр",
             "csv_file": "analytics/salaries_by_year_filtered.csv"},
            {"title": "Статистика по годам", "csv_file": "analytics/salaries_by_year.csv"},
        ]
        tables_html = [pd.read_csv(table["csv_file"]).to_html(classes='table', index=False, justify='left') for table in
                       manual_tables]
        titles = [table["title"] for table in manual_tables]
    else:
        tables_html = [
            pd.read_csv(io.StringIO(table.csv_file.read().decode('utf-8'))).to_html(classes='table', index=False,
                                                                                    justify='left') for table in tables]
        titles = [table.title for table in tables]
    return render(request, 'demand.html', {'plots': plots, 'tables': zip(titles, tables_html)})


def geography(request):
    plots = Image.objects.filter(category=Image.Category.GEOGRAPHY)
    tables = DataTable.objects.filter(category=DataTable.Category.GEOGRAPHY)
    if not tables:
        manual_tables = [
            {"title": "Доля вакансий по городам для разработчика игр",
             "csv_file": "analytics/vacancies_by_city_filtered.csv"},
            {"title": "Доля вакансий по городам", "csv_file": "analytics/vacancies_by_city.csv"},
            {"title": "Зарплаты по городам", "csv_file": "analytics/salaries_by_city.csv"},
            {"title": "Зарплаты по городам для разработчика игр",
             "csv_file": "analytics/salaries_by_city_filtered.csv"},
        ]
        tables_html = [pd.read_csv(table["csv_file"]).to_html(classes='table', index=False, justify='left') for table in
                       manual_tables]
        titles = [table["title"] for table in manual_tables]
    else:
        tables_html = [
            pd.read_csv(io.StringIO(table.csv_file.read().decode('utf-8'))).to_html(classes='table', index=False,
                                                                                    justify='left') for table in tables]
        titles = [table.title for table in tables]
    return render(request, 'geography.html', {'plots': plots, 'tables': zip(titles, tables_html)})


def skills(request):
    skills = Image.objects.filter(category=Image.Category.SKILL)
    tables = DataTable.objects.filter(category=DataTable.Category.SKILL)
    if not tables:
        manual_tables = [
            {"title": "20 самых популярных навыков по годам",
             "csv_file": "analytics/skills_by_year.csv"},
            {"title": "20 самых популярных навыков по годам для разработчика игр",
             "csv_file": "analytics/skills_by_year_filtered.csv"},
        ]
        tables_html = [pd.read_csv(table["csv_file"]).to_html(classes='table', index=False, justify='left') for table in
                       manual_tables]
        titles = [table["title"] for table in manual_tables]
    else:
        tables_html = [
            pd.read_csv(io.StringIO(table.csv_file.read().decode('utf-8'))).to_html(classes='table', index=False,
                                                                                    justify='left') for table in tables]
        titles = [table.title for table in tables]
    return render(request, 'skills.html', {'skills': skills, 'tables': zip(titles, tables_html)})


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
