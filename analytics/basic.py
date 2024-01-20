import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


vacancies = pd.read_csv('vacancies.csv')
vacancies['salary_from'] = vacancies['salary_from'].astype('float32')
vacancies['salary_to'] = vacancies['salary_to'].astype('float32')
rates= pd.read_csv('rates.csv')
float64_cols=list(rates.select_dtypes(include=['float64']))
rates[float64_cols]=rates[float64_cols].astype('float32')

def calculate_salary(row, currency):
    if pd.notna(row['salary']) and row['salary_currency'] != 'RUR':
        date_match = currency[currency['date'] == row['date']].index[0]
        currency_rate = currency.at[date_match, row['salary_currency']]
        if currency_rate:
            return row['salary'] * currency_rate
    return row['salary']

# добавление нужных полей
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], utc=True)
vacancies['year'] = vacancies['published_at'].dt.year
vacancies['salary'] = vacancies[['salary_from', 'salary_to']].mean(axis=1)
vacancies['key_skills'] = vacancies['key_skills'].str.split('\n')
vacancies['date'] = vacancies['published_at'].dt.strftime('01/%m/%Y')
vacancies['salary'] = vacancies.apply(calculate_salary, axis=1, args=(rates,))

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
city_percentage = vacancies['area_name'].value_counts(normalize=True)
cities_to_include = city_percentage[city_percentage >= 0.01].index
salary_by_city = vacancies[vacancies['area_name'].isin(cities_to_include)].groupby('area_name')['salary'].mean()
vacancies_by_city = vacancies.groupby('area_name').size().to_frame('vacancy')
vacancies_by_city['vacancy'] = round(vacancies_by_city['vacancy'] / vacancies.shape[0] * 100, 2)
salary_by_city_filtered = vacancies_filtered[vacancies_filtered['area_name'].isin(cities_to_include)].groupby('area_name')['salary'].mean()
vacancies_by_city_filtered = vacancies_filtered.groupby('area_name').size().to_frame('vacancy')
vacancies_by_city_filtered['vacancy'] = round(vacancies_by_city_filtered['vacancy'] / vacancies_filtered.shape[0] * 100, 2)


# Навыки
skills_by_year = vacancies.explode('key_skills').groupby('year')['key_skills'].value_counts().groupby('year').nlargest(
    20)
skills_by_year_filtered = vacancies_filtered.explode('key_skills').groupby('year')['key_skills'].value_counts().groupby(
    'year').nlargest(20)

skills_by_year_filtered.to_csv('skills_by_year_filtered.csv')
skills_by_year.to_csv('skills_by_year.csv')

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
plt.savefig('DjangoApp/static/images/plots/salary_by_year.png')
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
plt.savefig('DjangoApp/static/images/plots/vacancies_by_year.png')
plt.show()

# География

plot1 = plt.subplot2grid((2, 2), (0, 0)) #круговая
plot2 = plt.subplot2grid((2, 2), (0, 1)) #круговая игры
plot3 = plt.subplot2grid((2, 2), (1, 0), colspan=2) #барх

salary_by_city_sorted = salary_by_city.sort_values(ascending=False).head(10)
salary_by_city_filtered_sorted = salary_by_city_filtered.sort_values(ascending=False).head(10)
as_list = salary_by_city_sorted.index.tolist()
as_list = [label.replace(' ', '\n') for label in as_list]
x = np.arange(len(as_list))
# fig, ax = plt.subplots(layout="constrained")
plot3.set_title('Уровень зарплат по городам')
plot3.barh(x + width / 2, salary_by_city_sorted, width, label="Все вакансии")
plot3.barh(x - width / 2, salary_by_city_filtered_sorted, width, label="Вакансии разработчика игр")
plot3.set_yticks(x, as_list)
plot3.set_yticklabels(as_list, fontsize=6, va='center', ha='right')
plot3.legend(loc='upper right')
# plt.savefig('C:/Users/tihan/PycharmProjects/djangoProjectUlearn/DjangoApp/static/images/plots/salary_by_city.png')
# plt.show()

# fig, ax = plt.subplots(layout="constrained")
top_10_city_ratio = vacancies_by_city.sort_values('vacancy', ascending=False).head(10)
other = 100 - top_10_city_ratio['vacancy'].sum()
new_dic = {'Другие': other}
new_dic.update(top_10_city_ratio['vacancy'].to_dict())
area_count_dic = new_dic
labels = list(area_count_dic.keys())
sizes = list(area_count_dic.values())
plot1.pie(sizes, labels=labels, textprops={'fontsize': 6})
plot1.set_title('Доля вакансий по городам')
plot1.axis('scaled')
# plt.savefig('C:/Users/tihan/PycharmProjects/djangoProjectUlearn/DjangoApp/static/images/plots/vacancies_by_city.png')
# plt.show()

# fig, ax = plt.subplots(layout="constrained")
top_10_city_ratio_filtered = vacancies_by_city_filtered.sort_values('vacancy', ascending=False).head(10)
other = 100 - top_10_city_ratio_filtered['vacancy'].sum()
new_dic = {'Другие': other}
new_dic.update(top_10_city_ratio_filtered['vacancy'].to_dict())
area_count_dic = new_dic
labels = list(area_count_dic.keys())
sizes = list(area_count_dic.values())
plot2.pie(sizes, labels=labels, textprops={'fontsize': 6})
plot2.set_title('Доля вакансий по городам для выбранной профессии')
plot2.axis('scaled')
plt.subplots_adjust(hspace=0.5)
plt.tight_layout()
plt.savefig(
    'DjangoApp/static/images/plots/vacancies_by_city_filtered.png')
plt.show()

salary_by_year.to_csv('salaries_by_year.csv')
vacancies_by_year.to_csv('vacancies_by_year.csv')
salary_by_year_filtered.to_csv('salary_by_year_filtered.csv')
vacancies_by_year_filtered.to_csv('vacancies_by_year_filtered.csv')

salary_by_city_filtered.to_csv('salaries_by_city_filtered.csv')
salary_by_city.to_csv('salaries_by_city.csv')
top_10_city_ratio_filtered.to_csv('vacancies_by_city_filtered.csv')
top_10_city_ratio.to_csv('vacancies_by_city.csv')


# Навыки
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

    plt.savefig(
        f'DjangoApp/static/images/plots/skills_by_year_{year}.png')
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

    plt.savefig(
        f'DjangoApp/static/images/plots/skills_by_year_filtered_{year}.png')
    plt.show()
