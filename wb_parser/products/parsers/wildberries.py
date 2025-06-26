import requests
from urllib.parse import quote
import json
from django.utils import timezone
from ..models import Product

WB_API_URL = "https://search.wb.ru/exactmatch/ru/common/v4/search"


def parse_wildberries_api(query, category=None, page=1, limit=100):
    params = {
        'ab_testing': 'false',
        'appType': 1,
        'curr': 'rub',
        'dest': -364763,  # Россия
        'lang': 'ru',
        'page': page,
        'query': quote(query),
        'resultset': 'catalog',
        'sort': 'popular',
        'spp': 30,
        'suppressSpellcheck': 'false',
    }

    if category:
        params['kind'] = category  # Дополнительная фильтрация по категории

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if not data.get('data', {}).get('products'):
            return False, "Не найдено товаров"

        for product in data['data']['products']:
            try:
                # Извлекаем только нужные данные
                product_data = {
                    'name': product.get('name', 'Без названия'),
                    'price': float(product.get('salePriceU', 0)) / 100,  # Переводим копейки в рубли
                    'sale_price': float(product.get('priceU', 0)) / 100 if product.get('priceU') else None,
                    'rating': product.get('reviewRating', 0),
                    'reviews_count': product.get('feedbacks', 0),
                    'product_id': product.get('id'),  # Сохраняем ID для ссылок
                    'brand': product.get('brand', ''),
                    'query': query
                }

                # Создаем или обновляем товар
                Product.objects.update_or_create(
                    product_id=product_data['product_id'],
                    defaults=product_data
                )

            except Exception as e:
                print(f"Ошибка обработки товара: {e}")
                continue

        return True, f"Обработано {len(data['data']['products'])} товаров"

    except Exception as e:
        return False, f"Ошибка: {str(e)}"