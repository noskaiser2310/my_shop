from django.urls import path
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart, name="cart"),  # Đổi thành "cart/"
    path("checkout/", views.checkout, name="checkout"),  # Đổi thành "checkout/"
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
