from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from products.models import Product
from products.api.serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from decimal import Decimal
from django.core.exceptions import ValidationError


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ['price', 'rating', 'reviews_count', 'created_at']
    search_fields = ['name', 'query']

    filterset_fields = {
        'price': ['gte', 'lte'],
        'rating': ['gte', 'lte'],
        'reviews_count': ['gte', 'lte'],
        'query': ['exact', 'icontains'],
    }

    def get_queryset(self):
        queryset = Product.objects.all()

        try:
            # Обрабатываем min_price
            min_price = self.request.query_params.get('min_price', '0')
            min_price = Decimal(min_price) if min_price.lower() != 'inf' else Decimal('0')

            # Обрабатываем max_price (используем очень большое число вместо inf)
            max_price = self.request.query_params.get('max_price', '1000000000')  # 10 млн. руб.
            max_price = Decimal(max_price) if max_price.lower() != 'inf' else Decimal('1000000000')

            # Остальные параметры
            min_rating = Decimal(self.request.query_params.get('min_rating', '0'))
            min_reviews = int(self.request.query_params.get('min_reviews', '0'))

        except (ValueError, ValidationError):
            return Product.objects.none()

        # Применяем фильтры (умножаем на 100, если цена хранится в копейках)
        queryset = queryset.filter(
            price__gte=int(min_price * 100),
            price__lte=int(max_price * 100),
            rating__gte=min_rating,
            reviews_count__gte=min_reviews
        )

        return queryset