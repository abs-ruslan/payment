from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('item/<int:id>/', item, name='item'),
    path('', item_list, name='item_list'),
    path('get_striple_config/', get_striple_config, name='get_striple_config'),
    path('buy/<int:id>/', buy, name='buy'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('add_item_to_order/<int:id>/', add_item_to_order, name='add_item_to_order'),
    path('order_pay/<int:id>/<slug:coupon_id>/', order_pay, name='order_pay'),
    path('order/', order, name='order'),
    path('generate_coupon/<int:percent_off>/', generate_coupon, name='generate_coupon'),
]