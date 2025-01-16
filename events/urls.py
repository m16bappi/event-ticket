from django.urls import path

from events.views.event import EventListCreateAPIView, EventRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", EventListCreateAPIView.as_view()),
    path("<int:pk>/", EventRetrieveUpdateDestroyAPIView.as_view()),
]
