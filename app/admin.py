from django.contrib import admin
from .models import Item,Category, Order, OrderItem, Payment

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
