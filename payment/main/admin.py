from django.contrib import admin
from .models import Item, Order, Coupon

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('price', )
admin.site.register(Item, ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_create', 'get_items', 'amount', 'is_paid', 'coupon')
    list_filter = ('time_create', 'items__name')
    list_editable = ('is_paid', 'coupon')
admin.site.register(Order, OrderAdmin)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('percent_off', 'coupon_code')
admin.site.register(Coupon, CouponAdmin)