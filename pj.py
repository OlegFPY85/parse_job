import requests
from bs4 import BeautifulSoup
import json

# URL для парсинга
url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

# Заголовки для запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


# Функция для получения и парсинга вакансий
def get_vacancies(url):
    vacancies = []
    page = 0

    while True:
        # Формируем URL с параметром страницы
        page_url = f"{url}&page={page}"
        response = requests.get(page_url, headers=headers)

        # Проверяем успешность запроса
        if response.status_code != 200:
            print("Ошибка при запросе:", response.status_code)
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Ищем все карточки вакансий
        vacancy_cards = soup.find_all('div', class_='serp-item')

        # Проверяем, есть ли вакансии на странице
        if not vacancy_cards:
            break

        for card in vacancy_cards:
            try:
                title_elem = card.find('a', class_='serp-item__title')
                title = title_elem.text.strip() if title_elem else "Не указано"
                link = title_elem['href'] if title_elem else "Не указана"
                company_elem = card.find('div', class_='vacancy-serp-item__meta-info-company')
                company = company_elem.text.strip() if company_elem else "Не указана"
                city_elem = card.find('span', {'data-qa': 'vacancy-serp__vacancy-address'})
                city = city_elem.text.strip() if city_elem else "Не указан"

                # Проверка на наличие ключевых слов
                if "Django" in title() or "Flask" in title():
                    salary_elem = card.find('span', class_='bloko-header-section-3')
                    salary = salary_elem.text.strip() if salary_elem else "Не указана"

                    vacancies.append({
                        "title": title,
                        "link": link,
                        "company": company,
                        "city": city,
                        "salary": salary
                    })
            except Exception as e:
                print(f"Error parsing card: {e}")

        page += 1

    return vacancies


# Записываем результат в JSON файл
def save_to_json(vacancies, filename='vacancies.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)


vacancies = get_vacancies(url)
save_to_json(vacancies)

print(f"Найдено вакансий: {len(vacancies)}")
