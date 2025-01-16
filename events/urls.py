from django.urls import path

from .views.event import EventListCreateAPIView, EventRetrieveUpdateDestroyAPIView
from .views.ticket import TicketCreateAPIView
from .views.order import IPNOrderConfirmAPIView

urlpatterns = [
    path("", EventListCreateAPIView.as_view()),
    path("<int:pk>/", EventRetrieveUpdateDestroyAPIView.as_view()),
    path("ticket/", TicketCreateAPIView.as_view()),
    path("<int:id>/ipn/", IPNOrderConfirmAPIView.as_view()),
]
