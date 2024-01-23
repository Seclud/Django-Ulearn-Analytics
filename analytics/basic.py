import pandas as pd

vacancies = pd.read_csv('vacancies.csv')
vacancies['salary_from'] = vacancies['salary_from'].astype('float32')
vacancies['salary_to'] = vacancies['salary_to'].astype('float32')
rates = pd.read_csv('rates.csv')
float64_cols = list(rates.select_dtypes(include=['float64']))
rates[float64_cols] = rates[float64_cols].astype('float32')


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
vacancies_by_city_filtered['vacancy'] = round(vacancies_by_city_filtered['vacancy'] / vacancies_filtered.shape[0] * 100,
                                              2)

# Навыки
skills_by_year = vacancies.explode('key_skills').groupby('year')['key_skills'].value_counts().groupby('year').nlargest(
    20)
skills_by_year_filtered = vacancies_filtered.explode('key_skills').groupby('year')['key_skills'].value_counts().groupby(
    'year').nlargest(20)

skills_by_year_filtered.to_csv('skills_by_year_filtered.csv')
skills_by_year.to_csv('skills_by_year.csv')

top_10_city_ratio = vacancies_by_city.sort_values('vacancy', ascending=False).head(10)
top_10_city_ratio_filtered = vacancies_by_city_filtered.sort_values('vacancy', ascending=False).head(10)

salary_by_year.to_csv('salaries_by_year.csv')
print(salary_by_year)
vacancies_by_year.to_csv('vacancies_by_year.csv')
print(vacancies_by_year)
salary_by_year_filtered.to_csv('salary_by_year_filtered.csv')
print(salary_by_year_filtered)
vacancies_by_year_filtered.to_csv('vacancies_by_year_filtered.csv')
print(vacancies_by_year_filtered)

salary_by_city_filtered.to_csv('salaries_by_city_filtered.csv')
print(salary_by_city_filtered)
salary_by_city.to_csv('salaries_by_city.csv')
print(salary_by_city)
top_10_city_ratio_filtered.to_csv('vacancies_by_city_filtered.csv')
print(top_10_city_ratio_filtered)
top_10_city_ratio.to_csv('vacancies_by_city.csv')
print(top_10_city_ratio)
