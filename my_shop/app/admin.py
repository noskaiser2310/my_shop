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
    list_display = ["customer", "first_name", "last_name", "address", "phone_number"]
    list_filter = ["customer"]


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "is_active",
        "is_staff",
        "is_superadmin",
        "last_login",
        "date_joined",
    )

    list_display_links = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "address",
    )
    readonly_fields = ("last_login", "date_joined")
    list_filter = ("is_active", "is_staff", "is_superadmin")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("date_joined",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_sub", "sub_category")
    list_filter = ("is_sub", "sub_category")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


# Đăng ký model với các tùy chỉnh
admin.site.register(Category, CategoryAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
