from django.db import transaction
from rest_framework import generics

from events.models import Ticket
from events.serializers.ticket import TicketSerializer


class TicketCreateAPIView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        