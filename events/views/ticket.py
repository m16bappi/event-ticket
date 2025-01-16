from rest_framework import generics
from rest_framework.response import Response

from events.models import Ticket
from events.models.order import PaymentMethodChoice
from events.services import OrderService
from events.serializers.ticket import TicketSerializer


class TicketCreateAPIView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()

        payment = OrderService.init(
            ticket=ticket,
            payment_method=PaymentMethodChoice.SSLCOMMERZ,
        )
        return Response(data=payment)
