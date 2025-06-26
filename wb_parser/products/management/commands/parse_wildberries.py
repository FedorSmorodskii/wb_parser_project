from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Парсит товары с Wildberries по заданному запросу'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Поисковый запрос (например, "ноутбук")')

    def handle(self, *args, **kwargs):
        query = kwargs['query']
        success, message = Product.parse_and_save(query)
        if success:
            self.stdout.write(self.style.SUCCESS(f"Успешно: {message}"))
        else:
            self.stdout.write(self.style.ERROR(f"Ошибка: {message}"))