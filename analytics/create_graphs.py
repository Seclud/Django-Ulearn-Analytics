import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

salaries_by_year = pd.read_csv('salaries_by_year.csv').set_index('Год')
salaries_by_year_filtered = pd.read_csv('salaries_by_year_filtered.csv').set_index('Год')

vacancies_by_year = pd.read_csv('vacancies_by_year.csv').set_index('Год')
vacancies_by_year_filtered = pd.read_csv('vacancies_by_year_filtered.csv').set_index('Год')

salaries_by_city = pd.read_csv('salaries_by_city.csv').set_index('Город')
salaries_by_city_filtered = pd.read_csv('salaries_by_city_filtered.csv').set_index('Город')

vacancies_by_city = pd.read_csv('vacancies_by_city.csv').set_index('Город')
vacancies_by_city_filtered = pd.read_csv('vacancies_by_city_filtered.csv').set_index('Город')

skills_by_year = pd.read_csv('skills_by_year.csv').set_index('Год')
top_skills = skills_by_year.groupby('Год').apply(lambda x: x.nlargest(5, 'Кол-во')).droplevel(level=0)
print(top_skills)
skills_by_year_filtered = pd.read_csv('skills_by_year_filtered.csv').set_index('Год')
top_skills_filtered = skills_by_year_filtered.groupby('Год').apply(lambda x: x.nlargest(5, 'Кол-во')).droplevel(level=0)
print(top_skills_filtered)

# Графики
# Востребованность
width = 0.4
x = np.arange(len(salaries_by_year))

fig, ax = plt.subplots(layout="constrained")
ax.bar(x + width / 2, salaries_by_year['Зарплата'], width=width, label="Средняя зарплата")
ax.bar(x - width / 2, salaries_by_year_filtered['Зарплата'], width=width, label="Средняя зарплата разработчика игр")
ax.set_ylabel('Зарплата')
ax.set_title('Уровень зарплаты по годам')
ax.set_xticks(x, salaries_by_year.index.tolist())
ax.set_xticklabels(salaries_by_year.index.tolist(), rotation='vertical', va='top')
ax.legend(loc='upper right')
plt.savefig(r'C:\Users\tihan\PycharmProjects\djangoProjectUlearn\DjangoApp\static\images\plots/salary_by_year.png')
plt.show()

fig, ax = plt.subplots(layout="constrained")
ax.bar(x + width / 2, vacancies_by_year['Вакансии'], width=width, label="Кол-во вакансий")
ax.bar(x - width / 2, vacancies_by_year_filtered['Вакансии'], width=width, label="Кол-во вакансий разработчика игр")
ax.set_ylabel('Кол-во вакансий')
ax.set_title('Кол-во вакансий по годам')
ax.set_xticks(x, vacancies_by_year.index.tolist())
ax.set_xticklabels(vacancies_by_year.index.tolist(), rotation='vertical', va='top')
ax.legend(loc='upper right')
ax.set_yscale('log')
plt.savefig(r'C:\Users\tihan\PycharmProjects\djangoProjectUlearn\DjangoApp\static\images\plots/vacancies_by_year.png')
plt.show()

# География
plot1 = plt.subplot2grid((2, 2), (0, 0))  # круговая
plot2 = plt.subplot2grid((2, 2), (0, 1))  # круговая игры
plot3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)  # барх

salary_by_city_sorted = salaries_by_city.sort_values(by=['Зарплата'], ascending=False).head(10)
salary_by_city_filtered_sorted = salaries_by_city_filtered.sort_values(by=['Зарплата'], ascending=False).head(10)
as_list = salary_by_city_sorted.index.tolist()
as_list = [label.replace(' ', '\n') for label in as_list]
x = np.arange(len(as_list))
# fig, ax = plt.subplots(layout="constrained")
plot3.set_title('Уровень зарплат по городам')
plot3.barh(x + width / 2, salary_by_city_sorted['Зарплата'], width, label="Все вакансии")
plot3.barh(x - width / 2, salary_by_city_filtered_sorted['Зарплата'], width, label="Вакансии разработчика игр")
plot3.set_yticks(x, as_list)
plot3.set_yticklabels(as_list, fontsize=6, va='center', ha='right')
plot3.legend(loc='upper right', prop={'size': 6})
# plt.savefig('C:/Users/tihan/PycharmProjects/djangoProjectUlearn/DjangoApp/static/images/plots/salary_by_city.png')
# plt.show()

# fig, ax = plt.subplots(layout="constrained")
top_10_city_ratio = vacancies_by_city
other = 100 - top_10_city_ratio['Вакансии'].sum()
new_dic = {'Другие': other}
new_dic.update(top_10_city_ratio['Вакансии'].to_dict())
area_count_dic = new_dic
labels = list(area_count_dic.keys())
sizes = list(area_count_dic.values())
plot1.pie(sizes, labels=labels, textprops={'fontsize': 6})
plot1.set_title('Доля вакансий по городам')
plot1.axis('scaled')
# plt.savefig('C:/Users/tihan/PycharmProjects/djangoProjectUlearn/DjangoApp/static/images/plots/vacancies_by_city.png')
# plt.show()

# fig, ax = plt.subplots(layout="constrained")
top_10_city_ratio_filtered = vacancies_by_city_filtered
other = 100 - top_10_city_ratio_filtered['Вакансии'].sum()
new_dic = {'Другие': other}
new_dic.update(top_10_city_ratio_filtered['Вакансии'].to_dict())
area_count_dic = new_dic
labels = list(area_count_dic.keys())
sizes = list(area_count_dic.values())
plot2.pie(sizes, labels=labels, textprops={'fontsize': 6})
plot2.set_title('Доля вакансий по городам\nдля выбранной профессии')
plot2.axis('scaled')
plt.tight_layout()
plt.savefig(
    r'C:\Users\tihan\PycharmProjects\djangoProjectUlearn\DjangoApp\static\images\plots/vacancies_by_city_filtered.png')
plt.show()

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
