from django.urls import path
from products.api.views import ProductListAPIView  # Измененный путь импорта

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='products-list'),
]