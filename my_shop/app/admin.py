from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email")  # Hiển thị các trường này trong danh sách
    search_fields = ("name", "email")  # Tìm kiếm theo các trường này


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "digital")  # Hiển thị các trường này
    list_filter = ("digital",)  # Bộ lọc theo trường digital


class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "date_order", "complete", "transaction_id")
    list_filter = ("complete",)
    search_fields = ("transaction_id",)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "order", "quantity", "date_added")


from django.contrib import admin
from .models import ShippingAddress


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ["customer", "order", "address", "city", "state", "zipcode"]


# Đăng ký model với các tùy chỉnh
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
