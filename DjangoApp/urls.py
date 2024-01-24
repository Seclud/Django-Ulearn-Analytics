from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('skills/', views.skills, name='skills'),
    path('last_vacancies/', views.last_vacancies, name='last_vacancies'),
    path('demand/', views.demand, name='demand'),
    path('geogrpahy/', views.geography, name='geography'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)