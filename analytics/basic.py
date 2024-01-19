import pandas as pd
import matplotlib.pyplot as plt

vacancies = pd.read_csv('vacancies.csv')

# добавление нужных полей
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], utc=True)
vacancies['year'] = vacancies['published_at'].dt.year
vacancies['salary'] = vacancies[['salary_from', 'salary_to']].mean()
vacancies['key_skills'] = vacancies['key_skills'].str.split(',')

# фильтрация выбранной
keywords = ['game', 'unity', 'игр', 'unreal', 'GameDev']
vacancies_filtered = vacancies[vacancies['name'].str.contains('|'.join(r'\b{}\b'.format(word) for word in keywords))]

# Востребованность
salary_by_year = vacancies.groupby('year')['salary'].mean()
vacancies_by_year = vacancies.groupby('year').size()

salary_by_year_filtered = vacancies_filtered.groupby('year')['salary'].mean()
vacancies_by_year_filtered = vacancies_filtered.groupby('year').size()

# География
salary_by_city = vacancies.groupby('area_name')['salary'].mean()
vacancies_by_city = vacancies.groupby('area_name').size()

salary_by_city_filtered = vacancies_filtered.groupby('area_name')['salary'].mean()
vacancies_by_city_filtered = vacancies_filtered.groupby('area_name').size()

# Навыки
skills_by_year = vacancies.explode('key_skills').groupby('year')['key_skills'].value_counts().groupby('year').nlargest(
    20)
skills_by_year_filtered = vacancies_filtered.explode('key_skills').groupby('year')['key_skills'].value_counts().groupby(
    'year').nlargest(20)

# Графики
# Востребованность
fig, ax = plt.subplots()
salary_by_year.plot(ax=ax, label='All vacancies')
salary_by_year_filtered.plot(ax=ax, label='GameDev vacancies')
plt.legend()
plt.savefig('salary_by_year.png')
plt.show()

fig, ax = plt.subplots()
vacancies_by_year.plot(ax=ax, label='All vacancies')
vacancies_by_year_filtered.plot(ax=ax, label='GameDev vacancies')
plt.legend()
plt.savefig('vacancies_by_year.png')
plt.show()

# География
fig, ax = plt.subplots()
salary_by_city[:10].plot(kind='bar', ax=ax, label='All vacancies')
salary_by_city_filtered[:10].plot(kind='bar', ax=ax, label='GameDev vacancies')
plt.legend()
plt.savefig('salary_by_city.png')
plt.show()

fig, ax = plt.subplots()
vacancies_by_city[:10].plot(kind='bar', ax=ax, label='All vacancies')
vacancies_by_city_filtered[:10].plot(kind='bar', ax=ax, label='GameDev vacancies')
plt.legend()
plt.savefig('vacancies_by_city.png')
plt.show()

# Навыки
fig, ax = plt.subplots()
skills_by_year.plot(kind='bar', ax=ax, label='All vacancies')
skills_by_year_filtered.plot(kind='bar', ax=ax, label='GameDev vacancies')
plt.legend()
plt.savefig('skills_by_year.png')
plt.show()
