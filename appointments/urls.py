from django.urls import path
from .views import AppointmentListCreateAPIView, AppointmentUpdateAPIView, AppointmentCancelAPIView

urlpatterns = [
    path('appointments/', AppointmentListCreateAPIView.as_view(), name='appointments-list-create'),
    path('appointments/<int:pk>/', AppointmentUpdateAPIView.as_view(), name='appointments-update'),
    path('appointments/<int:pk>/cancel/', AppointmentCancelAPIView.as_view(), name='appointments-cancel'),
]




