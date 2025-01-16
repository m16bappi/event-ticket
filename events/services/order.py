from events.models import Ticket, SSLCommerzDatum
from events.models.order import Order, PaymentMethodChoice, OrderStatusChoice

from .ssl_commerz import SSLCommerzPayment


class OrderService:
    def __init__(self, order: Order):
        self.order = order

    @classmethod
    def init(cls, ticket: Ticket, payment_method: PaymentMethodChoice):
        order = Order.objects.create(
            ticket=ticket,
            amount=ticket.event.ticket_price,
            payment_method=payment_method,
        )

        payment_service = cls(order).get_payment_service()
        return payment_service.init(ticket)

    def confirm(self, validate_id: str):
        payment_service = self.get_payment_service()
        data = payment_service.validate(val_id=validate_id)

        if data.get("status") == "VALID":
            self.order.status = OrderStatusChoice.CONFIRMED
            self.order.save(update_fields=["status"])
            self.create_payment_datum(data=data)
        else:
            self.reject()

    def reject(self):
        self.order.status = OrderStatusChoice.FAILED
        self.order.save(update_fields=["status"])

    def cancel(self):
        self.order.status = OrderStatusChoice.CANCELLED
        self.order.save(update_fields=["status"])

    def get_payment_service(self):
        if self.order.payment_method == PaymentMethodChoice.SSLCOMMERZ:
            return SSLCommerzPayment()

    def create_payment_datum(self, data: dict):
        if self.order.payment_method == PaymentMethodChoice.SSLCOMMERZ:
            try:
                datum = SSLCommerzDatum.objects.create(
                    order=self.order,
                    val_id=data.get("val_id"),
                    tran_date=data.get("tran_date"),
                    currency=data.get("currency"),
                    amount=data.get("amount"),
                    store_amount=data.get("store_amount"),
                    card_type=data.get("card_type"),
                    card_no=data.get("card_no"),
                    bank_tran_id=data.get("bank_tran_id"),
                    tran_id=data.get("tran_id"),
                    status=data.get("status"),
                    currency_type=data.get("currency_type"),
                    currency_amount=data.get("currency_amount"),
                    currency_rate=data.get("currency_rate"),
                    base_fair=data.get("base_fair"),
                    error=data.get("error"),
                )
                return datum
            except Exception as e:
                print(e)
