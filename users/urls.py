from django.urls import path
from .views import RegisterView, LoginView

from .views import DoctorProfileView, DoctorListView

from .views import DoctorProfileCreateUpdateView, DoctorProfileListView, DoctorProfileSearchView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('doctors/manage/', DoctorProfileView.as_view(), name='doctor-manage'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),

    path('doctors/', DoctorProfileListView.as_view(), name='doctor-list'),
    path('doctors/manage/', DoctorProfileCreateUpdateView.as_view(), name='doctor-create-update'),
    path('doctors/search/', DoctorProfileSearchView.as_view(), name='doctor-search'),

]


