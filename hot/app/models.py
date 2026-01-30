from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# from app.models import cart


class Car(models.Model):
    name = models.CharField(max_length=100)  # Car name
    description = models.TextField()         # Car description
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price in dollars
    image = models.ImageField(upload_to='cars/')  # Image of the car
    created_at = models.DateTimeField(auto_now_add=True)  # When added
    stock = models.IntegerField()
    def __str__(self):
        return self.name  # Useful for admin display

class Wishlist(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
# ---
class Car(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='cars/')
    stock = models.IntegerField(null=True)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ---------------- CART ----------------

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    car = models.ForeignKey('Car', on_delete=models.CASCADE)  # Assuming your product model is Car
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.car.name}"
  
# ---------------- WISHLIST ----------------

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.user.username}'s Wishlist"


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    SUCCESS = "SUCCESS", _("Success")
    FAILED = "FAILED", _("Failed")


class Order(models.Model):
    name = models.CharField(
        _("Customer Name"),
        max_length=254
    )

    amount = models.DecimalField(
        _("Amount"),
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        _("Payment Status"),
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    # Razorpay / UPI order id (created BEFORE payment)
    provider_order_id = models.CharField(
        _("Provider Order ID"),
        max_length=100,
        blank=True,
        null=True
    )

    # Filled AFTER successful payment
    payment_id = models.CharField(
        _("Payment ID"),
        max_length=100,
        blank=True,
        null=True
    )

    signature_id = models.CharField(
        _("Signature ID"),
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name} - {self.status}"
