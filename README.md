# Проект по аналитике данных вакансий
Это проект по аналитике данных профессий. Он выложен на PythonAnywhere и доступен [тут](http://seclud.pythonanywhere.com/)
![image](https://github.com/Seclud/Django-Ulearn-Analytics/assets/82933148/693b3a7a-8bf0-4e06-ac92-ff017b4415fa)




## Структура проекта
Проект структурирован следующим образом:

- `analytics/`: Этот каталог содержит различные скрипты Python для анализа данных и файлы CSV с данными.
- `DjangoApp/`: Этот каталог содержит приложение Django.
- `djangoProjectUlearn/`: Этот каталог содержит настройки проекта Django..
- `templates/`: Этот каталог содержит шаблоны страниц Django.

## Анализ данных

Каталог `analytics/` содержит скрипты Python для анализа данных:

- `basic.py`: Содержит обработку большого файла vacancies
- `create_graphs`: На основе обработанного датасета создает графики
- `get_rates.py`: Парсит курсы валют с сайта ЦБР
- `parser test.py`: Тестовый парсер для api hh.ru, полноценно внедрен в last_vacancies
