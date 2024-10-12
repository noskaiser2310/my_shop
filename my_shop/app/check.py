import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_shop.my_shop.settings")
django.setup()

from app.models import OrderItem

# Lấy tất cả OrderItem không có sản phẩm liên kết
order_items_without_products = OrderItem.objects.filter(product__isnull=True)

print(order_items_without_products)
