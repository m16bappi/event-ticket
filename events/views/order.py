from rest_framework import views, status
from rest_framework.response import Response

from events.models import Order
from events.services import OrderService


class IPNOrderConfirmAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=kwargs["id"])
        except Order.DoesNotExist:
            return Response(data="order not found", status=status.HTTP_404_NOT_FOUND)

        order_service = OrderService(order)
        order_service.confirm(validate_id=request.data.get("val_id"))
        return Response(data="success")
