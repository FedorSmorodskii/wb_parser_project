from django.core.management.base import BaseCommand
from products.services.parsing_service import parse_and_save_products


class Command(BaseCommand):
    help = 'Поиск товаров на Wildberries через API'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Поисковый запрос')
        parser.add_argument('--category', type=int, help='ID категории', default=None)
        parser.add_argument('--page', type=int, default=1, help='Номер страницы')
        parser.add_argument('--limit', type=int, default=100, help='Лимит товаров')

    def handle(self, *args, **options):
        success, message = parse_and_save_products(
            query=options['query'],
            category=options['category'],
            page=options['page'],
            limit=options['limit']
        )

        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))