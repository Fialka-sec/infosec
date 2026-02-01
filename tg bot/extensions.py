# extensions.py
import requests
import json

class APIException(Exception):
    pass

class CryptoConverter:
    # Множество допустимых валют
    CURRENCIES = {
        'евро': 'EUR',
        'доллар': 'USD',
        'рубль': 'RUB'
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        base_code = CryptoConverter.CURRENCIES.get(base.lower())
        quote_code = CryptoConverter.CURRENCIES.get(quote.lower())

        if base_code is None:
            raise APIException(f'Валюта "{base}" не поддерживается.')
        if quote_code is None:
            raise APIException(f'Валюта "{quote}" не поддерживается.')
        if base_code == quote_code:
            raise APIException('Операция невозможна — одинаковые валюты.')
        if amount <= 0:
            raise APIException('Количество должно быть больше нуля.')

        # Запрос к API
        url = f'https://api.exchangerate-api.com/v4/latest/{base_code}'
        response = requests.get(url)
        if response.status_code != 200:
            raise APIException('Ошибка при обращении к валютному API.')
        data = response.json()

        if 'rates' not in data or quote_code not in data['rates']:
            raise APIException('Не удалось получить курс валют.')
        rate = data['rates'][quote_code]
        result = rate * amount
        return round(result, 2)