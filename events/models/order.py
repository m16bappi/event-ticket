from django.db import models
from django.contrib import admin

from .ticket import Ticket


class OrderStatusChoice(models.TextChoices):
    INIT = "INIT", "Init"
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"
    FAILED = "FAILED", "Failed"


class PaymentMethodChoice(models.TextChoices):
    SSLCOMMERZ = "SSLCOMMERZ", "SSLCommerz"


class Order(models.Model):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="order",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method = models.CharField(choices=PaymentMethodChoice, max_length=10)
    status = models.CharField(
        max_length=10,
        choices=OrderStatusChoice,
        default=OrderStatusChoice.INIT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket.name}"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("ticket", "amount", "status", "created_at")
    list_filter = ("status",)
