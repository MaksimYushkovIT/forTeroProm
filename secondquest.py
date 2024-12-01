import requests
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
url = "https://exchange-rates.abstractapi.com/v1/live/"
api_key = os.getenv("API_KEY")


params = {
    "api_key": api_key,
    "base": "RUB",
    "target": "USD,EUR,CNY"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    exchange_rates = data.get("exchange_rates", {})
    table_data = [
        ["Валюта", "Курс в RUB"],
        ["USD (доллар)", 1 / exchange_rates.get("USD", "Нет данных")],
        ["EUR (евро)", 1 / exchange_rates.get("EUR", "Нет данных")],
        ["CNY (юань)", 1 / exchange_rates.get("CNY", "Нет данных")]
    ]
    df = pd.DataFrame(table_data[1:], columns=table_data[0]) 
    print(df)
else:
    print(f"Ошибка: {response.status_code} - {response.text}")