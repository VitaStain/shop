from django.contrib import admin

from .models import (Brand, CallBack, Category, Order, Order_Product, Product,
                     Profile, Review, Shop, Shop_Product, Stock, Value,
                     ValueName, VirtualOrder)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'body_review', 'product', 'is_published']
    list_editable = ['is_published']


admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Shop_Product)
admin.site.register(Stock)
admin.site.register(ValueName)
admin.site.register(Value)
admin.site.register(VirtualOrder)
admin.site.register(Order)
admin.site.register(CallBack)
admin.site.register(Order_Product)
admin.site.register(Brand)
admin.site.register(Review, ReviewAdmin)
