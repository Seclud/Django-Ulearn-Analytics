from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('todos/', views.todos, name="Todos"),
    path('skills/', views.skills, name='skills'),
    path('last_vacancies/', views.last_vacancies, name='last_vacancies'),
]