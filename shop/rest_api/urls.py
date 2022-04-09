from django.urls import include, path
from rest_framework import routers

from .views import ProductViewSet, StockViewSet

app_name = 'rest_api'

product = routers.SimpleRouter()
product.register(r'product', ProductViewSet)

stock = routers.SimpleRouter()
stock.register(r'stock', StockViewSet)

urlpatterns = [
    path('', include(product.urls)),
    path('', include(stock.urls)),
]
