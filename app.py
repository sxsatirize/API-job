import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, render_template
import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import logging

app = Flask(__name__)

# Установим уровень логирования на DEBUG
logging.basicConfig(level=logging.DEBUG)

def get_vacancies(text, area, pages=1, per_page=100):
    api_url = 'https://api.hh.ru/vacancies'
    headers = {
        "User-Agent": "JobSearcher/1.0 (support@jobsearcher.com)",
        "HH-User-Agent": "JobSearcher/1.0 (support@jobsearcher.com)"
    }
    all_vacancies = []
    for page in range(pages):
        params = {
            'text': text,
            'area': area,
            'page': page,
            'per_page': per_page
        }
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        all_vacancies.extend(data['items'])
    return all_vacancies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/regions')
def regions():
    try:
        df_regions = pd.read_csv('../regions.hh/regions.csv')
        regions = df_regions.to_dict(orient="records")
        return render_template('regions.html', regions=regions)
    except Exception as e:
        logging.error(f"Error loading regions: {e}")
        return f"Error loading regions: {e}"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        search_text = request.form['text']
        region = request.form['region']
        logging.debug(f"Received search_text: {search_text}, region: {region}")

        status = "Идёт обработка данных..."
        vacancies = get_vacancies(search_text, region)
        logging.debug(f"Number of vacancies fetched: {len(vacancies)}")

        df = pd.DataFrame(vacancies)

        df['salary_from'] = df['salary'].apply(lambda x: x['from'] if x and 'from' in x else None)
        df['salary_to'] = df['salary'].apply(lambda x: x['to'] if x and 'to' in x else None)
        df['salary_currency'] = df['salary'].apply(lambda x: x['currency'] if x and 'currency' in x else None)
        df['employer_name'] = df['employer'].apply(lambda x: x['name'] if x and 'name' in x else None)
        df['area_name'] = df['area'].apply(lambda x: x['name'] if x and 'name' in x else None)

        df = df[['name', 'area_name', 'salary_from', 'salary_to', 'salary_currency', 'employer_name', 'published_at']]
        df = df.dropna(subset=['salary_from', 'salary_to'])
        df['salary_from'] = pd.to_numeric(df['salary_from'])
        df['salary_to'] = pd.to_numeric(df['salary_to'])

        plt.figure(figsize=(12, 6))
        bins = np.linspace(df['salary_from'].min(), df['salary_to'].max(), 20)
        plt.hist(df['salary_from'], bins=bins, alpha=0.5, label='Зарплата от', color='blue', edgecolor='black')
        plt.hist(df['salary_to'], bins=bins, alpha=0.5, label='Зарплата до', color='orange', edgecolor='black')
        plt.xlabel('Зарплата (руб)')
        plt.ylabel('Количество вакансий')
        plt.xticks(bins, rotation=45)
        plt.yticks(np.arange(0, df.shape[0] + 1, 1))
        plt.legend(loc='upper right')
        plt.title(f'Распределение зарплат для {search_text} в регионе {region}')
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('index.html', results=True, plot_url=plot_url, status=status)
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        return f"Error during analysis: {e}"

if __name__ == '__main__':
    app.run(debug=True)
