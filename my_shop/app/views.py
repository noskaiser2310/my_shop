from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

# Create your views here.


def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    categories = Category.objects.filter(is_sub=False)

    content = {
        "products": products,
        "categories": categories,  # Thêm danh mục vào context
    }
    return render(request, "app/home.html", content)


def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get("category", "")

    if active_category:
        products = Product.objects.filter(category__slug=active_category)

    return render(
        request,
        "app/category.html",
        {"categories": categories, "products": products, "active": active_category},
    )


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
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
    categories = Category.objects.filter(is_sub=False)
    content = {"items": items, "order": order, "categories": categories}
    return render(request, "app/cart.html", content)


def checkout(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
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
            "categories": categories,
        }
        return render(request, "app/checkout.html", context)

    else:
        return redirect(
            "login"
        )  # Chuyển hướng đến trang đăng nhập nếu người dùng chưa đăng nhập


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    if orderItem.quantity <= 0:
        orderItem.delete()
    else:
        orderItem.save()

    return JsonResponse(
        {"message": "Item was updated", "quantity": orderItem.quantity}, safe=False
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # Sử dụng UserCreationForm
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserCreationForm()

    content = {"form": form}
    return render(request, "app/register.html", content)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Here we log in the user
            messages.success(request, "Logged in successfully!")
            return redirect("home")  # Redirect to a home or dashboard page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "app/login.html")


@login_required
def home_view(request):
    # Logic cho trang chính của bạn
    return render(request, "app/home.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


def search(request):
    query = request.GET.get("q")  # Lấy từ khóa tìm kiếm từ query string
    results = []
    categories = Category.objects.filter(is_sub=False)
    if query:
        results = Product.objects.filter(
            name__icontains=query
        )  # Tìm kiếm theo tên sản phẩm

    context = {
        "query": query,
        "results": results,
        "categories": categories,
    }

    return render(request, "app/search.html", context)


def detail(request, productId):
    product = Product.objects.get(id=productId)
    categories = Category.objects.filter(is_sub=False)
    return render(
        request, "app/detail.html", {"product": product, "categories": categories}
    )
