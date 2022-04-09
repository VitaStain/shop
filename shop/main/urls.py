from django.urls import path

from .views import (CatalogView, CategoryList, Main_page, ProductDetailView,
                    ReviewCreate, ReviewList, SearchListView)

app_name = 'main'

urlpatterns = [
    path('', Main_page.as_view(), name='main_page'),
    path('category/', CategoryList.as_view(), name='category'),
    path('category/<int:pk>', CatalogView.as_view(), name='catalog'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='productdetail'),
    path('review/<int:pk>', ReviewList.as_view(), name='review'),
    path('reviewcreate/<int:pk>', ReviewCreate.as_view(), name='reviewcreate'),
    path('search/', SearchListView.as_view(), name='search')
]
