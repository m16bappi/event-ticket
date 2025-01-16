from django.db import models
from django.contrib import admin

from .order import Order


class SSLCommerzDatum(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="sslcommerz_datum",
    )
    val_id = models.CharField(max_length=100, null=True)
    tran_date = models.DateTimeField(null=True)
    currency = models.CharField(max_length=10, null=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18, null=True)
    store_amount = models.DecimalField(max_digits=36, decimal_places=18, null=True)
    card_type = models.CharField(max_length=100, null=True)
    card_no = models.CharField(max_length=100, null=True)
    bank_tran_id = models.CharField(max_length=100, null=True)
    tran_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    currency_type = models.CharField(max_length=100, null=True)
    currency_amount = models.DecimalField(max_digits=36, decimal_places=18, null=True)
    currency_rate = models.DecimalField(max_digits=36, decimal_places=18, null=True)
    base_fair = models.DecimalField(max_digits=36, decimal_places=18, null=True)
    error = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order}"


@admin.register(SSLCommerzDatum)
class SSLCommerzDatumAdmin(admin.ModelAdmin):
    list_display = ("order", "val_id", "tran_date", "amount", "status")
    list_filter = ("status",)
