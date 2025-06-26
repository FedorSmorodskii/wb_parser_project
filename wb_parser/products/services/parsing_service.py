from ..models import Product
from ..api.wildberries_api import parse_wildberries_api

def parse_and_save_products(query, category=None, page=1, limit=100):
    """Универсальная функция для парсинга и сохранения товаров"""
    return parse_wildberries_api(
        query=query,
        category=category,
        page=page,
        limit=limit
    )