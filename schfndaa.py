from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re
import random

def google_scholar_search(query):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме без GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Инициализация драйвера
    service = ChromeService(executable_path='/usr/local/bin/chromedriver')  # Укажите путь к ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    results_count = 0

    try:
        # Открытие страницы Google Scholar с запросом
        driver.get(f"https://scholar.google.com/scholar?q={query}")
        time.sleep(2)  # Задержка для загрузки страницы

        # Извлечение текста о количестве результатов
        result_stats = driver.find_element(By.XPATH, '//div[contains(text(), "Результатов: примерно")]')
        result_text = result_stats.text
        
        # Используем регулярное выражение для извлечения числа результатов
        match = re.search(r'Результатов: примерно ([\d\s\xa0]+)', result_text)
        if match:
            number_of_results = match.group(1).replace(' ', '').replace('\xa0', '')
            results_count = int(number_of_results) if number_of_results else 0

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()  # Закрытие драйвера

    return results_count

# Запросы для поиска по биосурфактантам и их методам на английском языке
queries = [
    "biosurfactants FTIR TLC",
    "biosurfactants NMR HPLC-MS",
    "biosurfactants FTIR TLC HPLC-MS",
    "lipopeptides FTIR",
    "lipopeptides TLC",
    "lipopeptides FTIR TLC",
    "lipopeptides FTIR TLC NMR HPLC-MS",
    "lipopeptides NMR",  # Новый запрос для липопептидов по NMR
    "lipopeptides HPLC-MS",  # Новый запрос для липопептидов по HPLC-MS
    "surfactin FTIR",
    "surfactin TLC",
    "surfactin FTIR TLC",
    "surfactin FTIR TLC NMR HPLC-MS",
    "surfactin NMR",  # Новый запрос для сурфактина по NMR
    "surfactin HPLC-MS",  # Новый запрос для сурфактина по HPLC-MS
    "glycolipids FTIR",
    "glycolipids TLC",
    "glycolipids FTIR TLC",
    "glycolipids FTIR TLC NMR HPLC-MS",
    "glycolipids NMR",  # Новый запрос для гликолипидов по NMR
    "glycolipids HPLC-MS",  # Новый запрос для гликолипидов по HPLC-MS
    "rhamnolipids FTIR",
    "rhamnolipids TLC",
    "rhamnolipids FTIR TLC",
    "rhamnolipids FTIR TLC NMR HPLC-MS",
    "rhamnolipids NMR",  # Новый запрос для рамнолипидов по NMR
    "rhamnolipids HPLC-MS"  # Новый запрос для рамнолипидов по HPLC-MS
]

# Словарь для хранения результатов
results = {}

# Выполнение поиска по каждому запросу
for query in queries:
    print(f"Searching for: {query}")
    count = google_scholar_search(query)
    
    if count == 0:
        print(f"No results found for: {query}")
    
    results[query] = count
    print(f"Results: {count}")
    
    time.sleep(random.uniform(5, 10))  # Случайная задержка от 5 до 10 секунд

# Создание DataFrame и сохранение в Excel файл
df = pd.DataFrame(list(results.items()), columns=['Query', 'Results'])
df.to_excel('scholar_search_results_biosurfactants.xlsx', index=False)
print("Results saved to scholar_search_results_biosurfactants.xlsx")