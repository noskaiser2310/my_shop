from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django import forms


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)  # Use set_password() to hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    # customer = models.ForeignKey(
    #     get_user_model(), on_delete=models.SET_NULL, blank=True, null=True
    # )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    # shipping_address = models.CharField(max_length=200, null=True)
    # shipping_phone_number = models.CharField(max_length=50, null=True)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        """Trả về tên đầy đủ của người dùng."""
        return f"{self.first_name} {self.last_name}"


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "email",
            # "shipping_address",
            # "shipping_phone_number",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "address"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "email"}
            ),
            # "shipping_address": forms.TextInput(
            #     attrs={"class": "form-control", "placeholder": "Shipping Address"}
            # ),
            # "shipping_phone_number": forms.TextInput(
            #     attrs={"class": "form-control", "placeholder": "Shipping Phone Number"}
            # ),
        }


class CreateUserForm(UserCreationForm):

    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class Category(models.Model):
    sub_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        null=True,
        blank=True,
    )
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name or "Unnamed Category"


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="product")
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)  # Ensure this is present

    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name if self.product else 'Unknown Product'}"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(Account):
    customer = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True
    )
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # address = models.CharField(max_length=200, null=True)
    # phone_number = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}, {self.address} ,{self.phone_number}"
        )
