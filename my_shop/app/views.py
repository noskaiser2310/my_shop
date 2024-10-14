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
        order = Order.objects.filter(customer=customer, complete=False).first()

        if order:
            items = order.orderitem_set.all()
        else:
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0}

    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
        }

    categories = Category.objects.filter(is_sub=False)
    content = {"items": items, "order": order, "categories": categories}
    return render(request, "app/cart.html", content)


def checkout(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.filter(customer=customer, complete=False).first()

        if order:
            items = order.orderitem_set.all()
            for item in items:
                item.total_price = item.product.price * item.quantity
        else:
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0}

        if request.method == "POST":

            shipping_address = ShippingAddress()
            shipping_address.customer = customer
            shipping_address.order = order
            shipping_address.name = request.POST["name"]
            shipping_address.email = request.POST["email"]
            shipping_address.address = request.POST["address"]
            shipping_address.save()
            order.complete = True
            order.save()

            return redirect("order_history")

        context = {
            "items": items,
            "order": order,
            "categories": categories,
        }
        return render(request, "app/checkout.html", context)

    else:
        return redirect("login")


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
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CreateUserForm()

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
    return render(request, "app/home.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


def search(request):
    query = request.GET.get("q")
    results = []
    categories = Category.objects.filter(is_sub=False)
    if query:
        results = Product.objects.filter(name__icontains=query)

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


def order_history(request):
    if request.user.is_authenticated:
        customer = request.user
        orders = Order.objects.filter(customer=customer, complete=True).order_by(
            "-date_order"
        )

        order_items = []
        for order in orders:
            items = order.orderitem_set.all()
            order_items.append((order, items))

    else:
        orders = []
        order_items = []

    context = {
        "orders": orders,
        "order_items": order_items,
    }

    return render(request, "app/order_history.html", context)


def account(request):
    if request.method == "POST":
        form = UserAccountForm(
            request.POST, instance=request.user
        )  # Đảm bảo bạn sử dụng đúng instance
        if form.is_valid():
            form.save()
            return redirect("account")  # Redirect sau khi lưu thành công
    else:
        form = UserAccountForm(instance=request.user)  # Để hiển thị thông tin hiện tại

    return render(request, "app/account.html", {"user_account_form": form})
