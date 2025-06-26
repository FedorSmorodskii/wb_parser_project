import requests
from django.utils import timezone
from ..models import Product

WB_API_URL = "https://search.wb.ru/exactmatch/ru/common/v13/search"


def parse_wildberries_api(query, category=None, page=1, limit=100):
    params = {
        'query': query,
        'page': page,
        'appType': 1,
        'curr': 'rub',
        'dest': -364763,
        'resultset': 'catalog',
        'sort': 'popular',
        'spp': 30,
    }

    try:
        response = requests.get(WB_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if not data.get('data', {}).get('products'):
            return False, "Не найдено товаров по данному запросу"

        saved_count = 0
        skipped_count = 0

        for product in data['data']['products'][:limit]:
            try:
                # Получаем информацию о цене (новый способ)
                sizes = product.get('sizes', [])
                if sizes:
                    price_info = sizes[0].get('price', {})
                    price = float(price_info.get('product', 0)) / 100  # product - цена со скидкой
                    basic_price = float(price_info.get('basic', 0)) / 100  # базовая цена
                else:
                    # Старый способ (на случай если sizes отсутствует)
                    price = float(product.get('salePriceU', 0)) / 100
                    basic_price = float(product.get('priceU', 0)) / 100

                # Проверяем валидность цены
                if price <= 0:
                    skipped_count += 1
                    continue

                # Формируем данные для сохранения
                product_data = {
                    'product_id': product['id'],
                    'name': product.get('name', ''),
                    'brand': product.get('brand', ''),
                    'price': price,
                    'sale_price': basic_price if basic_price > price else None,
                    'rating': product.get('rating', 0),
                    'reviews_count': product.get('feedbacks', 0),
                    'query': query,
                    'created_at': timezone.now(),
                }

                # Сохраняем товар
                Product.objects.update_or_create(
                    product_id=product['id'],
                    defaults=product_data
                )
                saved_count += 1

            except Exception as e:
                print(f"Ошибка при обработке товара {product.get('id')}: {str(e)}")
                continue

        return True, f"Успешно сохранено {saved_count} товаров, пропущено {skipped_count}"

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {str(e)}")
        return False, f"Ошибка API: {str(e)}"