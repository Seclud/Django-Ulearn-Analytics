import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

vacancies = pd.read_csv('vacancies.csv')

# добавление нужных полей
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], utc=True)
vacancies['year'] = vacancies['published_at'].dt.year
vacancies['salary'] = vacancies[['salary_from', 'salary_to']].mean(axis=1)
vacancies['key_skills'] = vacancies['key_skills'].str.split('\n')

# фильтрация выбранной
keywords = ['game', 'unity', 'игр', 'unreal', 'GameDev']
vacancies_filtered = vacancies[vacancies['name'].str.contains('|'.join(r'\b{}\b'.format(word) for word in keywords))]

# Востребованность
salary_by_year = vacancies.groupby('year')['salary'].mean()
vacancies_by_year = vacancies.groupby('year').size()

salary_by_year_filtered = vacancies_filtered.groupby('year')['salary'].mean()
salary_by_year_filtered = salary_by_year_filtered.reindex(salary_by_year.index, fill_value=0)
vacancies_by_year_filtered = vacancies_filtered.groupby('year').size()
vacancies_by_year_filtered = vacancies_by_year_filtered.reindex(salary_by_year.index, fill_value=0)

# География
salary_by_city = vacancies.groupby('area_name')['salary'].mean()
vacancies_by_city = vacancies.groupby('area_name').size()

salary_by_city_filtered = vacancies_filtered.groupby('area_name')['salary'].mean()
vacancies_by_city_filtered = vacancies_filtered.groupby('area_name').size()

# Навыки
# print(vacancies.explode('key_skills'))
# print(vacancies.explode('key_skills').groupby('year')['key_skills'].value_counts())
# print(vacancies.explode('key_skills').groupby('year')['key_skills'].value_counts().nlargest(20))
skills_by_year = vacancies.explode('key_skills').groupby('year')['key_skills'].value_counts().groupby('year').nlargest(20)
#skills_by_year = vacancies.explode('key_skills').groupby('year')['key_skills'].value_counts().reset_index().sort_values(by=[year,],ascending=False)
skills_by_year_filtered = vacancies_filtered.explode('key_skills').groupby('year')['key_skills'].value_counts().groupby(
    'year').nlargest(20)

# Графики
# Востребованность
width = 0.4
x = np.arange(len(salary_by_year))

fig, ax = plt.subplots(layout="constrained")
ax.bar(x + width / 2, salary_by_year, width=width, label="Средняя зарплата")
ax.bar(x - width / 2, salary_by_year_filtered, width=width, label="Средняя зарплата разработчика игр")
ax.set_ylabel('Зарплата')
ax.set_title('Уровень зарплаты по годам')
ax.set_xticks(x, salary_by_year.index.tolist())
ax.set_xticklabels(salary_by_year.index.tolist(), rotation='vertical', va='top')
ax.legend(loc='upper right')
plt.savefig('salary_by_year.png')
plt.show()

fig, ax = plt.subplots(layout="constrained")
ax.bar(x + width / 2, vacancies_by_year, width=width, label="Кол-во вакансий")
ax.bar(x - width / 2, vacancies_by_year_filtered, width=width, label="Кол-во вакансий разработчика игр")
ax.set_ylabel('Кол-во вакансий')
ax.set_title('Кол-во вакансий по годам')
ax.set_xticks(x, vacancies_by_year.index.tolist())
ax.set_xticklabels(vacancies_by_year.index.tolist(), rotation='vertical', va='top')
ax.legend(loc='upper right')
ax.set_yscale('log')
plt.savefig('vacancies_by_year.png')
plt.show()

# География
x = np.arange(len(salary_by_city[:10]))
fig, ax = plt.subplots(layout="constrained")
ax.bar(x + width / 2, salary_by_city[:10], width=width, label="Все вакансии")
ax.bar(x - width / 2, salary_by_city_filtered[:10], width=width, label="Вакансии разработчика игр")
ax.legend(loc='upper right')
plt.savefig('salary_by_city.png')
plt.show()

fig, ax = plt.subplots(layout="constrained")
ax.bar(x + width / 2, vacancies_by_city[:10], width=width, label="Все вакансии")
ax.bar(x - width / 2, vacancies_by_city_filtered[:10], width=width, label="Вакансии разработчика игр")
ax.legend(loc='upper right')
plt.savefig('vacancies_by_city.png')
plt.show()

# Навыки
# x = np.arange(len(skills_by_year))
# fig, ax = plt.subplots(layout="constrained")
# ax.bar(x + width / 2, skills_by_year, width=width, label="Все вакансии")
# ax.bar(x - width / 2, skills_by_year_filtered, width=width, label="Вакансии разработчика игр")
# ax.legend(loc='upper right')
# plt.savefig('skills_by_year.png')
# plt.show()
# Get unique years
years = skills_by_year.index.get_level_values(0).unique()

# Ширина столба
width = 0.35

# Цикл через года для всех профессий
for year in years:
    # Данные за этот год
    skills_this_year = skills_by_year.loc[year]

    # Обрезать ярылки до 20 знаков
    labels = [label[:20] + '...' if len(label) > 20 else label for label in
              skills_this_year.index.get_level_values('key_skills').tolist()]

    # Посчитать распределение вдоль x
    x = np.arange(len(skills_this_year))

    # Создать график
    fig, ax = plt.subplots(layout="constrained")
    ax.bar(x, skills_this_year, width, label='Все вакансии')

    # Лейблы, название и легенда
    ax.set_ylabel('Количество')
    ax.set_title(f'Топ 20 навыков в {year} году')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation='vertical')
    ax.legend()

    plt.savefig(f'skills_by_year_{year}.png')
    plt.show()

# Цикл через года для отфильтрованных профессий
for year in years:
    # Данные за этот год
    skills_this_year_filtered = skills_by_year_filtered.loc[year]


    # Обрезать ярылки до 20 знаков
    labels = [label[:20] + '...' if len(label) > 20 else label for label in
              skills_this_year_filtered.index.get_level_values('key_skills').tolist()]

    # Посчитать распределение вдоль x
    x = np.arange(len(skills_this_year_filtered))

    # Создать график
    fig, ax = plt.subplots(layout="constrained")
    ax.bar(x, skills_this_year_filtered, width, label='Вакансии разработчика игр')

    # Лейблы, название и легенда
    ax.set_ylabel('Количество')
    ax.set_title(f'Топ 20 навыков в {year} году')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation='vertical')
    ax.legend()

    plt.savefig(f'skills_by_year_filtered_{year}.png')
    plt.show()

skills_by_year.style