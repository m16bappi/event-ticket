from django.db import models
from django.contrib import admin

from .event import Event


class TicketStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"


class Ticket(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10,
        choices=TicketStatus,
        default=TicketStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.event.name}"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("name", "event", "status", "created_at")
