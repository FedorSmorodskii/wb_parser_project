from django.db import models


class Product(models.Model):
    product_id = models.BigIntegerField(unique=True)  # ID из Wildberries
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(default=0)
    reviews_count = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)
    query = models.CharField(max_length=255)  # Поисковый запрос
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.name}"

    def get_absolute_url(self):
        return f"https://www.wildberries.ru/catalog/{self.product_id}/detail.aspx"

    @classmethod
    def parse_and_save(cls, query):
        from .services.parsing_service import parse_and_save_products
        return parse_and_save_products(query)