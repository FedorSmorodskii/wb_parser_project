from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sale_price', 'rating', 'reviews_count', 'query')
    list_filter = ('rating', 'query')
    search_fields = ('name', 'query')
    actions = ['parse_selected_queries']

    def parse_selected_queries(self, request, queryset):
        """Кастомное действие для парсинга выбранных запросов."""
        for product in queryset.distinct('query'):
            success, message = Product.parse_and_save(product.query)
            self.message_user(request, f"Парсинг для '{product.query}': {message}")
    parse_selected_queries.short_description = "Запустить парсинг для выбранных запросов"