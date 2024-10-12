from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "digital")  # Hiển thị các trường này
    list_filter = ("digital",)  # Bộ lọc theo trường digital


class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "date_order", "complete", "transaction_id")
    list_filter = ("complete",)
    search_fields = ("transaction_id",)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "order", "quantity", "date_added")


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ["customer", "order", "address", "city", "state", "zipcode"]


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_active",
        "last_login",
        "date_joined",
    )

    list_display_links = ("email", "username", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = ("date_joined",)


# Đăng ký model với các tùy chỉnh
admin.site.register(Account, AccountAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
