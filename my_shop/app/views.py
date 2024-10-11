from django.shortcuts import render, redirect
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from django.http import HttpResponse

# Create your views here.


def home(request):
    products = Product.objects.all()
    content = {"products": products}
    return render(request, "app/home.html", content)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # Lấy đơn hàng gần đây nhất của khách hàng chưa hoàn thành
        order = Order.objects.filter(customer=customer, complete=False).first()

        if order:  # Nếu có đơn hàng chưa hoàn thành
            items = order.orderitem_set.all()  # Lấy tất cả các item trong order
        else:  # Nếu không có đơn hàng nào, tạo context rỗng
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0}

    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
        }  # Giá trị mặc định khi người dùng chưa đăng nhập

    # Tạo context là một dict chứa items và order
    content = {"items": items, "order": order}
    return render(request, "app/cart.html", content)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()

        if order:  # Nếu có đơn hàng chưa hoàn thành
            items = order.orderitem_set.all()
            for item in items:
                item.total_price = (
                    item.product.price * item.quantity
                )  # Tính tổng giá trị cho mỗi mặt hàng
        else:
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0}

        if request.method == "POST":
            # Xử lý thông tin từ form
            shipping_address = ShippingAddress()
            shipping_address.customer = customer
            shipping_address.order = order
            shipping_address.name = request.POST["name"]
            shipping_address.email = request.POST["email"]
            shipping_address.address = request.POST["address"]
            shipping_address.city = request.POST["city"]
            shipping_address.state = request.POST["state"]
            shipping_address.zipcode = request.POST["zipcode"]
            shipping_address.country = request.POST["country"]
            shipping_address.save()

            # Đánh dấu đơn hàng là hoàn thành
            order.complete = True
            order.save()

            # Chuyển hướng đến trang xác nhận hoặc trang khác
            return redirect(
                "confirmation"
            )  # Thay 'confirmation' bằng tên url thực tế của bạn

        context = {
            "items": items,
            "order": order,
        }
        return render(request, "app/checkout.html", context)

    else:
        return redirect(
            "login"
        )  # Chuyển hướng đến trang đăng nhập nếu người dùng chưa đăng nhập
