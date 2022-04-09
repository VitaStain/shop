from django.urls import path

from .views import (OrderCreate, OrderDetail, OrderList, VirtualOrderCreate,
                    call_back, cart_add, cart_detail, cart_remove,
                    comparison_add, comparison_detail, comparison_remove,
                    favorites_add, favorites_detail, favorites_remove)

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('comparison/', comparison_detail, name='comparison_detail'),
    path('favorites/', favorites_detail, name='favorites_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('comparison_add/<int:product_id>/', comparison_add, name='comparison_add'),
    path('favorites_add/<int:product_id>/', favorites_add, name='favorites_add'),
    path('comparison_remove/<int:product_id>/', comparison_remove, name='comparison_remove'),
    path('favorites_remove/<int:product_id>/', favorites_remove, name='favorites_remove'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('orderoneclick/', VirtualOrderCreate.as_view(), name='virtual_order'),
    path('order/', OrderCreate.as_view(), name='order'),
    path('orderdetail/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('order_list/', OrderList.as_view(), name='order_list'),
    path('call-back/', call_back, name='call_back')
]
