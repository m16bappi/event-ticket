from events.models import Ticket
from .ssl_commerz import SSLCommerzPayment
from events.models.order import Order, PaymentMethodChoice


class OrderService:
    def __init__(self, order: Order):
        self.order = order

    @classmethod
    def init(cls, ticket: Ticket, payment_method: PaymentMethodChoice):
        order: Order = ticket.order.create(
            amount=ticket.event.ticket_price,
            payment_method=payment_method,
        )

        payment_service = cls(order).get_payment_service()
        return payment_service.init(ticket)

    def confirm(self): ...
    def reject(self): ...

    def get_payment_service(self):
        if self.order.payment_method == PaymentMethodChoice.SSLCOMMERZ:
            return SSLCommerzPayment
