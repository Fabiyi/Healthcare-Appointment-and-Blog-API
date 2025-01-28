from django.urls import path, include
from .views import AppointmentCreateView, AppointmentListView, AppointmentUpdateView

urlpatterns = [
    path('', AppointmentCreateView.as_view(), name='appointment-create'),
    path('list/', AppointmentListView.as_view(), name='appointment-list'),
    path('<int:pk>/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/', include('appointments.urls')),
]



