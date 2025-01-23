from django.urls import path
from .views import RegisterView, LoginView

from .views import DoctorProfileView, DoctorListView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('doctors/manage/', DoctorProfileView.as_view(), name='doctor-manage'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
]


